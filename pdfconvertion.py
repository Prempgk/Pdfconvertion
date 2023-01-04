from typing import List
import pdfkit
from fastapi import FastAPI, BackgroundTasks, File
from fastapi.responses import StreamingResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, Required
from datetime import date, time, datetime

templates = Jinja2Templates(directory="templates")

# Need to install wkhtmltopdf and need to add a bin path to system environment variables
# For windows: https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_msvc2015-win64.exe
# For Ubuntu/Debian: sudo apt-get install wkhtmltopdf

# configuration to store a pdf file
config = pdfkit.configuration(wkhtmltopdf="C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")

# Initializing fast api app
app = FastAPI()


class ticket_data(BaseModel):
    Booking_id: str = Field(min_length=5, max_length=20)
    Booked_on: datetime
    Company_name: str = Field(min_length=5, max_length=100)
    Company_logo: str
    Plane_name: str = Field(min_length=3, max_length=20)
    From_date: date
    From_time: time
    From_city: str = Field(min_length=3, max_length=50)
    From_platform: str = Field(min_length=5, max_length=100)
    From_airport_address: str = Field(min_length=5, max_length=100)
    Booking_class: str = Field(min_length=3, max_length=50)
    To_date: date
    To_time: time
    To_platform: str = Field(min_length=5, max_length=100)
    To_city: str = Field(min_length=3, max_length=50)
    Time_diff: str
    To_airport_address: str = Field(min_length=5, max_length=100)
    Traveller_details: List


@app.post('/ticket/pdf/')
async def pdf_convertion(data: ticket_data):
    sub_data = templates.get_template('ticket.html').render({"data": data})
    pdfkit.from_string(sub_data, 'output.pdf', configuration=config, options={"enable-local-file-access": True})
    f = 'C:/Users/Anicha/PycharmProjects/rupi/output.pdf'
    return FileResponse(f)


@app.get('/pdf')
async def pdf():
    f = 'C:/Users/Anicha/PycharmProjects/rupi/output.pdf'
    return FileResponse(f)
