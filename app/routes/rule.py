"""Routes for user rules"""
from fastapi import APIRouter, Request, HTTPException, Depends
from typing import List

from app.security import security_authentication
from app.models.rule import Rule, ResourceRule

router = APIRouter(responses={
    401: {"description": "unauthorized/Invalid authentication"},
    403: {"description": "Forbidden/Do not have access to resource/operation"}
})


@router.get('/resource/{resource_id}', response_model=List[ResourceRule])
async def ger_resource_rules(request: Request, resource_id: str, security_profile=Depends(security_authentication)):
    """Get rules for a resource"""
    if resource := await request.app.db.get_resource_by_id(resource_id):
        # Check if user has permission
        if not (await security_profile.check_permissions(resource_account_id=resource.account_id, level=0)):
            raise HTTPException(status_code=403, detail="Invalid Permissions")
        rules_aggregation = await request.app.db.rules_by_resource_type_pipeline(resource.resource_type_id)
        non_compliance = await request.app.db.get_non_complaince_by_resource_id(resource.id)
        exceptions = await request.app.db.get_exception_from_exception_value(resource.reference)
        # List Comprehension to get list of rules non-compliant & rule exceptions
        non_compliant_rule_id = [n.rule_id for n in non_compliance]
        exception_rules_id = []
        # Check exception is not suspended before enabling
        for x in exceptions:
            if not x.exception.suspended:
                exception_rules_id.append(x.rule_resource_type.rule.id)
        return_list = []
        for rule_pipline in rules_aggregation:
            # Check if rule is compliant or not
            compliant, exception = True, False
            if rule_pipline.rule.id in non_compliant_rule_id:
                compliant = False
            # See if rule has exception
            if rule_pipline.rule.id in exception_rules_id:
                exception = True
            return_list.append({
                "id": rule_pipline.rule.id,
                "name": rule_pipline.rule.name,
                "description": rule_pipline.rule.description,
                "compliant": compliant,
                "exception": exception,
                "resource_type": {
                    "id": rule_pipline.resource_type.id,
                    "name": rule_pipline.resource_type.name,
                    "platform": {
                        "id": rule_pipline.platform.id,
                        "name": rule_pipline.platform.name,
                    }
                }
            })
        return return_list
    else:
        raise HTTPException(status_code=404, detail="Resource not found")
