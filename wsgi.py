# from app import app as application

# app = application

# if __name__ == "__main__":
#     application.run(host='0.0.0.0', port=6378)



import os
import uvicorn
from app import app as application

port = "6378"
uvicorn.run(application, host="0.0.0.0", port=port) 