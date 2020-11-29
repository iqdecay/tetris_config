// Build the API url to be called based on environment variables
function getApiUrl(endpoint) {
    // The endpoint must NOT start or end with a '/' character
    const baseUrl = "http://" + process.env.REACT_APP_BACKEND_URL + ":" + process.env.REACT_APP_BACKEND_PORT + "/"
    return baseUrl + endpoint + "/"
}

export default getApiUrl