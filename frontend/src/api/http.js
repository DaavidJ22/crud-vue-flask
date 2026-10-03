import axios from 'axios'

const http = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})

http.interceptors.response.use(
  (response) => response,
  (requestError) => {
    requestError.message =
      requestError.response?.data?.error || 'No fue posible comunicarse con el servidor'
    return Promise.reject(requestError)
  },
)

export default http
