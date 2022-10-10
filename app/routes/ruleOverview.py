"""Routes for rules overview"""
from fastapi import APIRouter, Request, HTTPException, Depends, Query
from typing import List
from dataclasses import asdict
from bson import ObjectId

from app.security import security_authentication
from app.models.ruleOverview import RuleOverview

router = APIRouter(responses={
    401: {"description": "unauthorized/Invalid authentication"},
    403: {"description": "Forbidden/Do not have access to resource/operation"}
})


@router.get('/{account_id}', response_model=List[RuleOverview])
async def get_rule_overview(request: Request, account_id: str, security_profile=Depends(security_authentication)):
    """Get an overview of rules"""
    # Check if user has permission
    if not (await security_profile.check_permissions(resource_account_id=account_id, level=0)):
        raise HTTPException(status_code=403, detail="Invalid Permissions")
    rules_pipeline = await request.app.db.get_all_rules_pipeline()
    non_compliant_resources_query = await request.app.db.get_non_compliant_resources_by_account_id(account_id)
    return_list = []
    # Build rules response
    for rule in rules_pipeline:
        # Get resource not compliant with rules
        non_compliant_resources: List[str] = []
        non_compliant_resources_object_id: List[ObjectId] = []
        for r in non_compliant_resources_query:
            if r.non_compliance.rule_id == rule.rule.id:
                non_compliant_resources.append(r.id)
                non_compliant_resources_object_id.append(r.object_id)

        compliant_resources = await request.app.db.get_resource_by_account_id_and_not_in_id_list(
            non_compliant_resources_object_id, account_id, rule.rule.resource_type_id)
        compliant_resource_ids = [x.id for x in compliant_resources]

        resource_type_dict = asdict(rule.resource_type)
        resource_type_dict["platform"] = asdict(rule.platform)
        rule_dict = asdict(rule.rule)
        rule_dict["resource_type"] = resource_type_dict

        return_list.append({
            "rule": rule_dict,
            "non_compliant": non_compliant_resources,
            "compliant": compliant_resource_ids,
        })
    return return_list
