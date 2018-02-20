from subprocess import call
import boto3


def handler(event, context):
    # Download reference data from source
    # call(["wget", "http://106.37.208.233:20035/emcpublish/ClientBin/Env-CnemcPublish-RiaServices-EnvCnemcPublishDomainService.svc/binary/GetAQIDataPublishLives", "-O", "GetAQIDataPublishLives"])

    # Run wcf2xml and send to data.xml
    f = open("data.xml", "w")
    call(["python", "python-wcfbin/wcf2xml.py", "GetAQIDataPublishLives"],
         stdout=f)

    # Convert data.xml to JSON and store in airnow.json
    call(["python", "xml2json.py"])

    # Save output file to S3
    data = open("/tmp/airnows.json", "rb")
    s3 = boto3.client('s3')
    s3.put_object(
        Body=data,
        ContentType="application/json",
        Bucket="openaq-chinaaqidata",
        Key="airnow.json"
    )

    return {
        'done': True
    }
