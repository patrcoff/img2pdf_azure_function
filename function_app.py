import azure.functions as func
import logging
import img2pdf

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="first_http_trigger_test")
def first_http_trigger_test(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
    
def convert_img_to_pdf(infile,outfile):
    """Convert image to pdf. img2pdf requires a file as input."""
    
    pdf_bytes = img2pdf.convert(infile)
    with open(outfile, 'wb') as file:
        file.write(pdf_bytes)

@app.route(route='tiff2pdf')
def convert_tiff2pdf(req: func.HttpRequest) -> func.HttpResponse:
# expects a request as below:
# with open('image.tif','rb) as f:
#    img = f.read()
#    requests.post(url,data=img)
    
    try:
        req_body = req.get_body()

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
    else:
        with open('imagefile.tif','wb') as f:
            f.write(req_body)
        
        convert_img_to_pdf('imagefile.tif','imagefile.pdf')
        # need to then send this to blob
        return func.HttpResponse(
                "This HTTP triggered function executed successfully.",
                status_code=200
            )

    