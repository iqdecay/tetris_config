
function getApiUrl(endpoint) {
    const endpointTrimmed = endpoint.trim("/")
    const baseUrl = "http://" + process.env.REACT_APP_BACKEND_URL + ":" + process.env.REACT_APP_BACKEND_PORT + "/"
    return baseUrl + endpointTrimmed + "/"
}
export default getApiUrl