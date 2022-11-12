import boto3
import argparse
import time
import cv2 as cv

def predict(net, img, h, w):
    blob = cv.dnn.blobFromImage(img, 1.0, (w, h),
                                (103.939, 116.779, 123.680), swapRB=False, crop=False)

    print('[INFO] Setting the input to the model')
    net.setInput(blob)

    print('[INFO] Starting Inference!')
    start = time.time()
    out = net.forward()
    end = time.time()
    print('[INFO] Inference Completed successfully!')

    # Reshape the output tensor and add back in the mean subtraction, and
    # then swap the channel ordering
    out = out.reshape((3, out.shape[2], out.shape[3]))
    out[0] += 103.939
    out[1] += 116.779
    out[2] += 123.680
    out /= 255.0
    out = out.transpose(1, 2, 0)

    # Printing the inference time
    print('[INFO] The model ran in {:.4f} seconds'.format(end - start))

    return out

# Source for this function:
# https://github.com/jrosebr1/imutils/blob/4635e73e75965c6fef09347bead510f81142cf2e/imutils/convenience.py#L65
def resize_img(img, width=None, height=None, inter=cv.INTER_AREA):
    dim = None
    h, w = img.shape[:2]

    if width is None and height is None:
        return img
    elif width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    elif height is None:
        r = width / float(w)
        dim = (width, int(h * r))

    resized = cv.resize(img, dim, interpolation=inter)
    return resized


def process_image(image, model, output):
    net = cv.dnn.readNetFromTorch(model)
    img = cv.imread(image)
    img = resize_img(img, width=600)
    h, w = img.shape[:2]
    out = predict(net, img, h, w)
    out = cv.convertScaleAbs(out, alpha=255.0)
    cv.imwrite(output, out)


'''def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image', type=str, help='path to the input image')
    parser.add_argument('-m', '--model', type=str, help='path to the model file')
    parser.add_argument('-o', '--output', type=str, help='path to the output image')
    args = parser.parse_args()
    process_image(args.image, args.model, args.output)'''

def handler(event, context):
    upload_bucket = 'upload-bucket-hw7'
    results_bucket = 'results-bucket-hw7'
    model_bucket = 'model-bucket-hw7'
    #image = event['messages'][0]['details']['object_id']
    image = event['messages'][0]['details']['message']['body']

    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id='nKRSTJ2RtVi5adaSim-_',
        aws_secret_access_key='gpzr1qkECWFfdNV798emZZBIsbNXdP3DLi-ehTJm'
    )

    # download model
    s3.download_file(model_bucket, 'mosaic.t7', '/tmp/model')

    # download pic
    s3.download_file(upload_bucket, image, '/tmp/image.jpg')

    # change pic
    process_image('/tmp/image.jpg', '/tmp/model', '/tmp/new-image.jpg')

    # upload it
    s3.upload_file('/tmp/new-image.jpg', results_bucket, image)


    return {
        'statusCode': 200,
        'body': 'Hello World!',
    }


