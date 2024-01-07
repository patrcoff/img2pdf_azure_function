# AZURE Function App to Convert Images (e.g. tif) to PDF

This Functions App takes an image as the body of an HTTP request, converts it to a PDF file and uploads it to blob storage.

It is intended to be called by a Logic App consumption as part of a broader automation workflow.

## Plan for the Logic App Workflow

We want the workflow to be easy to trigger by the key stakeholder (my wife) without any technical knowledge requirements.

Likely, by emailing the file to be converted to a specific email address would be the easiest usage for the user.

As such, my prvovisional plan is as follows:

- User emails provided address with attachment of image to be converted
- Check if attachment present and of correct file format
- Email user if no attachment or not an image
- Call Function App with file content in request.

In a separate Logic App:

- poll a blob container for new file uploads
- email user the file when it is uploaded.