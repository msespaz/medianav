import unittest
from tv.models import Show, Episode, VideoFile

class CoreModelTest(unittest.TestCase):
    """ Test the models contained in the 'core' app 
    """
    def setUp(self):
        self.show = Show(name="Test Show")
        self.show.save()
        self.episode = Show(name="Test Episode")
        self.episode.save()
        self.video_file = VideoFile(name="Test Video File")
        self.video_file.save()

    def tearDown(self):
        self.show.delete()
        self.episode.delete()
        self.video_file.delete()

    def testModels(self):
        self.assertEquals(self.show.name, "Test Show")
        self.assertEquals(self.episode.name, "Test Episode")
        self.assertEquals(self.video_file.name, "Test Video File")

