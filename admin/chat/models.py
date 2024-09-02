import uuid
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Room Model
class Room(models.Model):
    # Room ka unique identifier UUID field se define kar rahe hain
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_user = models.ForeignKey(User, related_name="room_first", on_delete=models.CASCADE, null=True)
    second_user = models.ForeignKey(User, related_name="room_second", on_delete=models.CASCADE, null=True)

# Message Model
class Message(models.Model):
    # Message model me user ko associate kar rahe hain
    user = models.ForeignKey(User, related_name="messages", verbose_name="User", on_delete=models.CASCADE)
    # Message ko room ke saath link kar rahe hain
    room = models.ForeignKey(Room, related_name="messages", verbose_name="Room", on_delete=models.CASCADE)
    # Message content ko text field me store kar rahe hain
    content = models.TextField(verbose_name="Message Content")
    # Message create hote hi uska timestamp auto add hota hai
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")  # Accurate timestamp ke liye DateTimeField use kiya
    what_is_it = models.CharField(max_length=50, null=True)

    def get_short_date(self):
        local_time = timezone.localtime(self.created_date)
        return local_time.strftime("%H:%M")

# CapturedImage Model
class CapturedImage(models.Model):
    # Captured image ko user ke saath link kar rahe hain
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Image field jo uploaded image ko store karega
    image = models.ImageField(upload_to='captured_images/')
    # Timestamp for when the image was created
    created_at = models.DateTimeField(auto_now_add=True)
