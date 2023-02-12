import Axios, {AxiosInstance} from 'axios'
import { getToken } from './token'

export class ApiClient {
  private client: AxiosInstance;

  constructor(baseURL: string) {
    this.client = Axios.create(
      {
        baseURL: baseURL,
        responseType: 'json' as const,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
      }
    )
 
    // Set the AUTH token for any request
    this.client.interceptors.request.use((config) => {
      const token = getToken()
      if (token && config.headers) {
        config.headers.Authorization = token;
      }
      return config;
    });
  }

  async get<TResponse>(path: string): Promise<TResponse> {
    const resp = await this.client.get<TResponse>(path)
    console.log(resp.data)
    return resp.data
  }

  async post<TRequest, TResponse>(path: string, req: TRequest): Promise<TResponse> {
    const resp = await this.client.post<TResponse>(path, req)
    console.log(resp.data)
    return resp.data
  }

  async delete<TResponse>(path: string): Promise<TResponse> {
    const resp = await this.client.delete<TResponse>(path)
    console.log(resp.data)
    return resp.data
  }

  async postUrlEncoded<TRequest, TResponse>(path: string, req: TRequest): Promise<TResponse> {
    const params = new URLSearchParams()
    for (const [k, v] of Object.entries(req as any)) {
      params.append(k as string, v as string)
    }
    const resp = await this.client.post<TResponse>(path, params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    return resp.data
  }

  async postForm<TRequest, TResponse>(path: string, req: TRequest): Promise<TResponse> {
    const resp = await this.client.post<TResponse>(path, req, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    return resp.data
  }
}

const apiClient = new ApiClient(process.env.VUE_APP_ROOT_API)
export default apiClient
