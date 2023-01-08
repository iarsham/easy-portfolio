from apps.extensions.test_setup import GeneralApiTestCase


class PortfolioModelTest(GeneralApiTestCase):

    def setUp(self):
        super().setUp()
        self.aboutme1 = self.user1.user_aboutme
        self.aboutme2 = self.user2.user_aboutme

    def test_aboutme_str_method(self):
        str_aboutme = f"{self.user1.user_aboutme.full_name} - {self.user1.username}"
        self.assertEqual(self.aboutme1.__str__(), str_aboutme)

    def test_fullname_property(self):
        aboutme_obj = self.aboutme2
        aboutme_obj.first_name, aboutme_obj.last_name = 'nick', 'jackson'
        aboutme_obj.save()
        self.assertEqual(aboutme_obj.full_name, 'nick jackson')

    def test_education_str_method(self):
        education_obj = self.aboutme2.about_education
        str_education = f"{self.user2.username} - {education_obj.field_study}"
        self.assertEqual(education_obj.__str__(), str_education)

    def test_skills_str_method(self):
        skill_obj = self.aboutme2.about_skill.create(
            name='python'
        )
        str_skill = f"{self.user2.username} - {skill_obj.name}"
        self.assertEqual(skill_obj.__str__(), str_skill)

    def test_language_str_method(self):
        language_obj = self.aboutme1.about_language.create(
            name='Dutch',
            proficiency='full-professional'
        )
        str_language = "%s - %s - %s" % (
            self.user1.username,
            language_obj.name,
            language_obj.proficiency
        )
        self.assertEqual(language_obj.__str__(), str_language)

    def test_achievement_str_method(self):
        achievement_obj = self.aboutme2.about_achieve.create(
            title='achievement title',
            description='achievement description'
        )
        str_achievement = f"{self.user2.username} - {achievement_obj.title}"
        self.assertEqual(achievement_obj.__str__(), str_achievement)

    def test_contact_me_str_method(self):
        contact_me_obj = self.user2.user_contact_me.create(
            name='Alex Ferguson',
            email='alex@email.com',
            subject='Next game plan :)',
            message='Hello guys'
        )
        str_achievement = f"{self.user2.username} - {contact_me_obj.email}"
        self.assertEqual(contact_me_obj.__str__(), str_achievement)
