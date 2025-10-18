import requests
import json
from smolagents import tool

@tool
def send_api_request(url: str, method: str = "GET", headers: dict = None, data: dict = None, params: dict = None) -> str:
    """A tool that sends HTTP requests to APIs at a specified URL.
    
    Args:
        url (str): The API endpoint URL to send the request to
        method (str): HTTP method (GET, POST, PUT, DELETE, etc.). Defaults to "GET"
        headers (dict): Optional headers to include in the request
        data (dict): Optional JSON data to send in the request body (for POST/PUT requests)
        params (dict): Optional query parameters to include in the URL
    
    Returns:
        str: The API response as a string, or an error message if the request fails
    """
    try:
        # Prepare headers
        if headers is None:
            headers = {}
        
        # Set default content-type for POST/PUT requests with data
        if method.upper() in ['POST', 'PUT'] and data and 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'
        
        # Send the request based on method
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, params=params, timeout=30)
        elif method.upper() == "POST":
            if data:
                response = requests.post(url, headers=headers, json=data, params=params, timeout=30)
            else:
                response = requests.post(url, headers=headers, params=params, timeout=30)
        elif method.upper() == "PUT":
            if data:
                response = requests.put(url, headers=headers, json=data, params=params, timeout=30)
            else:
                response = requests.put(url, headers=headers, params=params, timeout=30)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers, params=params, timeout=30)
        elif method.upper() == "PATCH":
            if data:
                response = requests.patch(url, headers=headers, json=data, params=params, timeout=30)
            else:
                response = requests.patch(url, headers=headers, params=params, timeout=30)
        else:
            return f"Unsupported HTTP method: {method}"
        
        # Check if request was successful
        if response.status_code >= 200 and response.status_code < 300:
            try:
                # Try to parse as JSON
                return json.dumps(response.json(), indent=2)
            except ValueError:
                # If not JSON, return as text
                return response.text
        else:
            return f"Request failed with status code {response.status_code}: {response.text}"
            
    except requests.exceptions.Timeout:
        return "Request timed out after 30 seconds"
    except requests.exceptions.ConnectionError:
        return f"Failed to connect to {url}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

@tool
def send_file_upload_request(url: str, file_path: str, field_name: str = "file", headers: dict = None, data: dict = None) -> str:
    """A tool that sends file upload requests to APIs.
    
    Args:
        url (str): The API endpoint URL to send the file to
        file_path (str): Path to the file to upload
        field_name (str): Form field name for the file. Defaults to "file"
        headers (dict): Optional headers to include in the request
        data (dict): Optional form data to include with the file
    
    Returns:
        str: The API response as a string, or an error message if the request fails
    """
    try:
        if headers is None:
            headers = {}
        
        # Prepare files for upload
        with open(file_path, 'rb') as f:
            files = {field_name: f}
            
            # Send POST request with file
            response = requests.post(
                url, 
                files=files, 
                data=data, 
                headers=headers, 
                timeout=60
            )
        
        # Check if request was successful
        if response.status_code >= 200 and response.status_code < 300:
            try:
                # Try to parse as JSON
                return json.dumps(response.json(), indent=2)
            except ValueError:
                # If not JSON, return as text
                return response.text
        else:
            return f"File upload failed with status code {response.status_code}: {response.text}"
            
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except requests.exceptions.Timeout:
        return "File upload timed out after 60 seconds"
    except requests.exceptions.ConnectionError:
        return f"Failed to connect to {url}"
    except requests.exceptions.RequestException as e:
        return f"File upload failed: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

@tool
def get_amazing_dog_fact() -> str:
    """A tool that tells you an amazing fact about dogs using a public API.
    Args: None
    """
    # URL for the public API
    url = "https://dogapi.dog/api/v2/facts"

    # case when there is a response from the API
    try:
        response = requests.get(url)
        if response.status_code == 200: # expected, okay status code
            # parsing response
            cool_dog_fact = response.json()['data'][0]['attributes']['body']
            return cool_dog_fact
        else:
            # in case of an unfavorable status code
            return "A dog fact could not be fetched."
    except requests.exceptions.RequestException as e:
        return "A dog fact could not be fetched."