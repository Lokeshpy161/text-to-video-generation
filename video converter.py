import imageio
import os
import cv2
import numpy as np

# Load keywords and image links from a text file
keywords_and_links = {}
with open("keyword.txt", "r") as file:
    for line in file:
        parts = line.strip().split(":")
        if len(parts) == 2:
            keyword, image_link = parts[0].strip(), parts[1].strip()
            keywords_and_links[keyword] = image_link

# Input keywords from the user
user_input = input("Enter keywords (comma-separated): ")
selected_keywords = [keyword.strip() for keyword in user_input.split(",")]

# List to store selected image filenames
selected_image_filenames = []

# Extract image filenames based on selected keywords
for keyword in selected_keywords:
    if keyword in keywords_and_links:
        selected_image_filenames.append(keywords_and_links[keyword])
    else:
        print(f"Keyword not found: {keyword}")

# Output video file
output_video = "output.mp4"

# Set the frame size (adjust as needed)
frame_width = 640
frame_height = 480

# Set the duration (in seconds) for each image (3 seconds)
image_duration = 3

# Set the duration (in seconds) for the transition animation (2 seconds)
transition_duration = 2

# Create a list to store image durations, including transitions
frame_durations = [image_duration] * len(selected_image_filenames)

# Add transition durations between images (except for the last image)
for i in range(len(selected_image_filenames) - 1):
    frame_durations.insert(i * 2 + 1, transition_duration)

# Initialize the video writer
video_writer = imageio.get_writer(output_video, fps=1)

# Loop through the selected image filenames and add them to the video
for i, image_filename in enumerate(selected_image_filenames):
    image = imageio.imread(image_filename)
    if image is not None:
        # Resize the image to match the frame size (if needed)
        if image.shape[0] != frame_height or image.shape[1] != frame_width:
            image = cv2.resize(image, (frame_width, frame_height))

        # Add the image to the video for the specified duration
        for _ in range(int(frame_durations[i])):
            video_writer.append_data(image)

        # Add a transition animation (crossfade) between images
        if i < len(selected_image_filenames) - 1:
            next_image = cv2.resize(imageio.imread(selected_image_filenames[i + 1]), (frame_width, frame_height))
            for j in range(int(transition_duration)):
                alpha = 1.0 - j / transition_duration
                blended_frame = cv2.addWeighted(image, alpha, next_image, 1.0 - alpha, 0)
                video_writer.append_data(blended_frame)
    else:
        print(f"Unable to load image: {image_filename}")

# Release the video writer
video_writer.close()

print("Video created successfully.")
