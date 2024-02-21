import os
import io
import pathlib
from parliament import Context
import boto3
import PIL
from diffusers import StableDiffusionInstructPix2PixPipeline, EulerAncestralDiscreteScheduler

in_endpoint = "http://" + os.environ["INPUTS_BUCKET_HOST"]
in_bucket = os.environ["INPUTS_BUCKET_NAME"]
in_s3 = boto3.client('s3',
    endpoint_url=in_endpoint,
    aws_access_key_id=os.environ["INPUTS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["INPUTS_SECRET_ACCESS_KEY"])

out_endpoint = "http://" + os.environ["OUTPUTS_BUCKET_HOST"]
out_bucket = os.environ["OUTPUTS_BUCKET_NAME"]
out_s3 = boto3.client('s3',
    endpoint_url=in_endpoint,
    aws_access_key_id=os.environ["OUTPUTS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["OUTPUTS_SECRET_ACCESS_KEY"])

model_id = "timbrooks/instruct-pix2pix"
pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(model_id, safety_checker=None)
pipe.to("cpu") # Change to cuda if you have a gpu
pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)

prompt = "turn it into a cartoon"

def read_input_image(key: str) -> PIL.Image:
    """
    Reads the image from the inputs bucket
    """
    print("Read input image")
    file_byte_string = in_s3.get_object(Bucket=in_bucket, Key=key)["Body"].read()
    image = PIL.Image.open(io.BytesIO(file_byte_string))
    image = PIL.ImageOps.exif_transpose(image)
    image = image.convert("RGB")
    print("Input image size is " + str(image.size))
    return image

def write_output_image(image: PIL.Image, key: str):
    """
    Writes the image to the output bucket
    """
    print("Write output image")
    print("Output image size " + str(image.size))
    # Save the image to an in-memory file
    file = io.BytesIO()
    file.name = pathlib.Path(key).name # Lets pillow figure out the file format
    image.save(file)
    file.seek(0)

    # Upload image to s3
    out_s3.upload_fileobj(file, out_bucket, key)
    print("File is uploaded")

def main(context: Context):
    """ 
    Called when uploading an image to in_bucket.
    Transforms the image using the prompt and uploads the result using out_bucket
    """
    if context.cloud_event is None:
        return "A cloud event is required", 400

    event_attributes = context.cloud_event.get_attributes()
    key = event_attributes['subject']
    print("Key is " + key)

    image = read_input_image(key)
    result_images = pipe(prompt, image=image, num_inference_steps=10, image_guidance_scale=1).images
    write_output_image(result_images[0], key)
    return "Done", 200
