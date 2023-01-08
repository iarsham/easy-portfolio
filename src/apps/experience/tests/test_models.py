from apps.extensions.test_setup import ExperienceApiTestCase
from apps.experience.models import Experience


class ExperienceModelTest(ExperienceApiTestCase):

    def setUp(self):
        super().setUp()
        self.experience2 = self.user2.experience_user.create(
            role="ReactJs FrontEnd Developer",
            employment_type="part-time",
            company_name="google.com",
            start_date="2020-02-01",
            end_date="2021-11-28",
            still_working=False
        )

    def test_experience_str_method(self):
        str_experience = "%s - %s - %s-%s - %s" % (
            self.experience2.role, self.user2.username,
            self.experience2.start_date, self.experience2.end_date,
            self.experience2.company_website_link
        )
        self.assertEqual(self.experience2.__str__(), str_experience)

    def test_experience_save_datetime(self):
        experience_obj = self.experience2
        experience_obj.still_working = True
        experience_obj.save()
        self.assertEqual(self.experience.end_date, None)

    def test_experience_slug_field(self):
        slug = "%s-%s-%s" % (
            self.user1.username,
            self.experience.role,
            self.experience.company_name
        )
        slug_expected = slug.lower().replace(' ', '-').replace('.', '')
        self.assertEqual(self.experience.slug, slug_expected)

    def test_experience_objects_ordering(self):
        last_object_created = Experience.objects.first()
        self.assertQuerysetEqual([last_object_created], [self.experience2])

    def test_project_str_method(self):
        str_project = "%s - %s - %s" % (
            self.user1.username,
            self.project.name,
            self.project.description[:15],
        )
        self.assertEqual(self.project.__str__(), str_project)

    def test_reference_str_method(self):
        str_reference = "%s - %s - %s" % (
            self.user2.username,
            self.reference.full_name,
            self.reference.email,
        )
        self.assertEqual(self.reference.__str__(), str_reference)

    def test_personal_project_str_method(self):
        str_personal_project = "%s - %s - %s" % (
            self.user1.username,
            self.personal_project.name,
            self.personal_project.link,
        )
        self.assertEqual(self.personal_project.__str__(), str_personal_project)

    def test_blog_str_method(self):
        str_blog = f"{self.user3.username} - {self.blog.title}"
        self.assertEqual(self.blog.__str__(), str_blog)
