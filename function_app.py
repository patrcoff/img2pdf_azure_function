import azure.functions as func
#from azure.functions import BlobServiceClient
import logging
import img2pdf
import base64

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# @app.route(route="first_http_trigger_test")
# def first_http_trigger_test(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')

#     name = req.params.get('name')
#     if not name:
#         try:
#             req_body = req.get_json()
#         except ValueError:
#             pass
#         else:
#             name = req_body.get('name')

#     if name:
#         return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
#     else:
#         return func.HttpResponse(
#              "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
#              status_code=200
#         )
    
# def convert_img_to_pdf(infile,outfile):
#     """Convert image to pdf. img2pdf requires a file as input."""
    
#     pdf_bytes = img2pdf.convert(infile)
#     with open(outfile, 'wb') as file:
#         file.write(pdf_bytes)

# def upload_blob_file(self, blob_service_client: BlobServiceClient, container_name: str):
#     container_client = blob_service_client.get_container_client(container=container_name)
#     with open(file=os.path.join('filepath', 'filename'), mode="rb") as data:
#         blob_client = container_client.upload_blob(name="sample-blob.txt", data=data, overwrite=True)

@app.function_name(name="tif2pdf")
@app.route(route='tiff2pdf')
def convert_tiff2pdf(req: func.HttpRequest) -> func.HttpResponse:
# expects a request as below:
# with open('image.tif','rb) as f:
#    img = f.read()
#    requests.post(url,data=img)
    
    try:
        req_body = req.get_json()

    except ValueError:
        logging.ERROR('Received request to \'tiff2pdf\' without request body!')
        return func.HttpResponse(
            "Missing payload - this endpoint expects an image payload in the request body.",
            status_code=400
        )
    except Exception as exc:
        logging.Error(f'Uhandled exception:\n {exc}')
        return func.HttpResponse(
            f'Something went wrong: \n{exc}',
            status_code=500
        )
    #else:
    #    img_content = req_body
        #tempFilePath = tempfile.gettempdir() # needed to enable temporary files in functions runtime
        # note, writing files normally works in local dev but not in functions runtime
        #fp = tempfile.NamedTemporaryFile()
        #with open(fp,'wb') as f:
        #fp = Path(tempFilePath) / 'imagefile'
        #    f.write(req_body)
    
    pdf_bytes = img2pdf.convert(base64.b64decode(req_body.get('ContentBytes')))
    return func.HttpResponse(body=base64.b64encode(pdf_bytes), status_code=200)
        
        #convert_img_to_pdf('imagefile.tif','imagefile.pdf')
        # with open('imagefile.pdf','rb') as f:
        #     img = f.read()
        #     return func.HttpResponse(body=
        #             "This HTTP triggered function executed successfully.",
        #             status_code=200
        #         )

    
