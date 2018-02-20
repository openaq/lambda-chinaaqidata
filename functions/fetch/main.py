from subprocess import call
import boto3
import requests
from subprocess import Popen, PIPE, STDOUT
import io


def handle(event, context):
    # Download reference data from source
    print("Downloading Chinese data")
    resp = requests.get("http://106.37.208.233:20035/emcpublish/ClientBin/Env-CnemcPublish-RiaServices-EnvCnemcPublishDomainService.svc/binary/GetAQIDataPublishLives")
    print("Data downloaded, saving locally")
    d = open("/tmp/GetAQIDataPublishLives", "wb")
    d.write(resp.content)
    d.close()

    # Run wcf2xml and send to data.xml
    print("Converting data to XML")
    f = open("/tmp/data.xml", "w")
    cmd = "python ChinaAQIData/python-wcfbin/wcf2xml.py /tmp/GetAQIDataPublishLives"
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.stdout.read()
    f.write(output.decode("utf-8"))
    f.close()

    # Convert data.xml to JSON and store in airnow.json
    print("Converting data to JSON")
    cmd = "python ChinaAQIData/xml2json.py /tmp/"
    p = Popen(cmd, shell=True, stdout=PIPE)
    p.wait()
    # output = p.stdout.read()
    # print(output)

    # f = open("/tmp/airnow.json", "r")
    # data = f.read()
    # print(data)
    # f.close()

    # Save output file to S3
    print("Saving data to S3")
    f = io.open("/tmp/airnow.json", "r", encoding="utf8")
    data = f.read()
    s3 = boto3.client('s3')
    s3.put_object(
        Body=data,
        ContentType="application/json",
        Bucket="openaq-chinaaqidata",
        Key="airnow.json"
    )
    f.close()

    return {
        'done': True
    }
