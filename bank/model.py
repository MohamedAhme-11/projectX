from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    institution = models.ForeignKey('Institution', on_delete=models.SET_NULL, null=True)
    account_type = models.ForeignKey('AccountType', on_delete=models.SET_NULL, null=True)
    # Setting a default value
    name_en = models.CharField(max_length=255, default='Default Name')
    name_ar = models.CharField(max_length=255, default='نص عربي')
    # Add related_name in groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_groups",  # Changed related_name
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_permissions",  # Changed related_name
        related_query_name="user",
    )





# Represents the legislative body responsible for setting educational criteria and standards.
class Legislator(models.Model):
    # models.py
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    name_en = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255, default='نص عربي')
    email = models.EmailField(max_length=254)
    location_branch_name_en = models.CharField(max_length=255, default="Default Branch Name")
    location_branch_name_ar = models.CharField(max_length=255, default="اسم الفرع الافتراضي")
    primary_contact_name = models.CharField(max_length=255, default="Default Contact Name")
    website = models.URLField(default="http://example.com")  # Provide a generic placeholder or relevant default URL
    country = models.CharField(max_length=100, default="Default Country")  # Provide a default country name
    governorate = models.CharField(max_length=100, default="Default Governorate")  # Provide a default governorate name
    city = models.CharField(max_length=100, default='Default City')
    phone = models.CharField(max_length=50, default="+01")  # Provide a default phone number or consider making it nullable
    landline = models.CharField(max_length=50, default="+02")  # Provide a default landline number or consider making it nullable
    show_on_qodourat = models.BooleanField(default=True)  # Set the default for showing on Qodourat as True or False depending on your needs
    
   

# Holds detailed descriptive and documentary information about various criteria.
class CriteriaDetail(models.Model):
    description_en = models.TextField()
    description_ar = models.TextField()
    document_link = models.URLField(blank=True, null=True)# Link to the document detailing the criteria
    version = models.CharField(max_length=50, null=True) # Versioning to track updates and changes

# Represents the specific criteria set by the legislator for faculties.
class FacultyCriteria(models.Model):
    name_en = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255, default='نص عربي')
    legislator = models.ForeignKey(Legislator, related_name='faculty_criteria', on_delete=models.CASCADE)
    detail = models.OneToOneField(CriteriaDetail, on_delete=models.CASCADE, null=True)# Links to CriteriaDetail for detailed description and documentation

# Represents the specific criteria for academic majors within faculties.
class MajorCriteria(models.Model):
    name_en = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255, default='نص عربي')
    faculty_criteria = models.ForeignKey(FacultyCriteria, related_name='major_criteria', on_delete=models.CASCADE)# Each major criteria is related to a broader faculty criteria
    detail = models.OneToOneField(CriteriaDetail, on_delete=models.CASCADE, null=True) # Links to CriteriaDetail for detailed description and documentation

class CourseCriteria(models.Model):
    name_en = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255, default='نص عربي')
    legislator = models.ForeignKey(Legislator, related_name='course_criteria', on_delete=models.CASCADE)
    detail = models.OneToOneField(CriteriaDetail, on_delete=models.CASCADE, null=True)  # Links to CriteriaDetail for detailed description and documentation


# Represents an educational institution like a university or college.
class Institution(models.Model):
    name_en = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255)
    url = models.URLField() 
    listed_by_mohesr = models.BooleanField()
    reviewed_by_legislator = models.BooleanField(default=False)
    accreditation_expiry_date = models.DateField()
    institute_category = models.ForeignKey('InstituteCategory', on_delete=models.CASCADE)
    account_type = models.ForeignKey('AccountType', on_delete=models.CASCADE)
    institution_type = models.ForeignKey('InstitutionType', on_delete=models.CASCADE)
    accreditation_status = models.ForeignKey('AccreditationStatus', on_delete=models.CASCADE)
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    selected_courses_taught = models.ManyToManyField('Course', related_name='institutions_taught')  # Renamed field
    selected_faculty_criteria = models.ManyToManyField(FacultyCriteria, related_name='institutions')
    selected_major_criteria = models.ManyToManyField(MajorCriteria, related_name='institutions')
    selected_course_criteria = models.ManyToManyField('CourseCriteria', related_name='institutions', blank=True)

    institution_selected_courses = models.ManyToManyField('Course', related_name='selected_institutions')

    # Rest of the model fields...

# Logs reviews and approvals of the institution's curriculum by the legislator.
class ReviewHistory(models.Model):
    institution = models.ForeignKey(Institution, related_name='review_history', on_delete=models.CASCADE)
    review_date = models.DateField()
    status = models.CharField(max_length=100)  # Tracks the status of the review
    comments = models.TextField(null=True, blank=True)# Any comments or notes from the review
    
# Represents a faculty within an institution, such as Engineering or Humanities.
class Faculty(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='faculties')
    name_en = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255, default='نص عربي')
    website_url = models.URLField()
    criteria = models.ForeignKey(FacultyCriteria, on_delete=models.SET_NULL, null=True, related_name='faculties')# Links faculty to a set of criteria defined by the legislator

# Defines a specific academic program or stream within a faculty.
class Program(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='programs')
    name_en = models.CharField(max_length=255, null=False)
    name_ar = models.CharField(max_length=255, default='نص عربي')

# Represents an academic major or specialization within a faculty.
class Major(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='majors')
    name_en = models.CharField(max_length=255, null=False)
    name_ar = models.CharField(max_length=255, default='نص عربي')
    criteria = models.ForeignKey(MajorCriteria, on_delete=models.SET_NULL, null=True, related_name='majors')# Links major to a set of criteria defined by the legislator


# Contains the intended learning outcomes for each major.


# Defines a course within a major, including its name and related major
class Course(models.Model):
    major = models.ForeignKey(Major, related_name='courses', on_delete=models.CASCADE)
    name_en = models.CharField(max_length=255, null=False)
    name_ar = models.CharField(max_length=255, default='نص عربي')
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True, related_name='courses_taught')  # Change related_name
    criteria = models.ForeignKey('CourseCriteria', on_delete=models.SET_NULL, null=True, related_name='courses')





# Represents a governorate or similar administrative region for location categorization.
class Governorate(models.Model):
    name_en = models.CharField(max_length=255, null=False)
    name_ar = models.CharField(max_length=255, default='نص عربي')

# Defines cities within governorates for further location specificity.
class City(models.Model):
    governorate = models.ForeignKey(Governorate, on_delete=models.CASCADE, related_name='cities')
    name_en = models.CharField(max_length=255, null=False)
    name_ar = models.CharField(max_length=255, default='نص عربي')

# Categorizes institutions, perhaps by their focus or funding nature.
class InstituteCategory(models.Model):
    name_en = models.CharField(max_length=255, null=False)
    name_ar = models.CharField(max_length=255, default='نص عربي')

# Likely represents different types of user accounts or institutional roles.
class AccountType(models.Model):
    name_en = models.CharField(max_length=255, null=False)
    name_ar = models.CharField(max_length=255, default='نص عربي')

# Categorizes institutions by type like university, college, vocational, etc.
class InstitutionType(models.Model):
    name_en = models.CharField(max_length=255, null=False)
    name_ar = models.CharField(max_length=255, default='نص عربي')

# Represents the accreditation status of an institution for regulatory purposes.
class AccreditationStatus(models.Model):
    status_en = models.CharField(max_length=255, null=False)
    status_ar = models.CharField(max_length=255, default='نص عربي')

