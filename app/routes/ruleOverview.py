"""Routes for user login & logout"""
from fastapi import APIRouter, Request, HTTPException, Depends, Query
from typing import List
from dataclasses import asdict

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
        HTTPException(status_code=403, detail="Invalid Permissions")
    rules = await request.app.db.get_all_rules()
    resources = await request.app.db.get_non_compliant_resources_by_account_id(account_id)
    return_list = []
    # Build rules response
    for rule in rules:
        # Get resource not compliant with rules
        non_compliant_resources: List[str] = []
        for r in resources:
            if r.non_compliance.rule_id == rule.id:
                non_compliant_resources.append(r.id)
        if resource_type := await request.app.db.get_resource_type_by_id(rule.resource_type_id):
            platform = await request.app.db.get_platform_by_id(resource_type.platform_id)
            resource_type_dict = asdict(resource_type)
            resource_type_dict["platform"] = asdict(platform)
            rule_dict = asdict(rule)
            rule_dict["resource_type"] = resource_type_dict
            return_list.append({
                "rule": rule_dict,
                "non_compliant": non_compliant_resources
            })
    return return_list
