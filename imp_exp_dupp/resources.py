# from django.contrib.auth.models import User
# from import_export import resources
# class RoleResourec(resources.ModelResource):
#         name = Field(attribute='username', column_name="username")
#         default_role = Field(attribute='default_role', column_name="System Role")
#         default_plan = Field(attribute='default_plan', column_name="System Plan")
        
#         class Meta:
#             models=User
#             fields= ('name', 'default_role', 'default_plan')
#             import_id_fields = ('name',)
#             skip_unchanged = True
