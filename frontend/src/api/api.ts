import Axios, {AxiosInstance} from 'axios'

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
}

const apiClient = new ApiClient(process.env.VUE_APP_ROOT_API)
export default apiClient
