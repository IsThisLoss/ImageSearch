import apiClient, {ApiClient} from './api'

interface UploadResponse {
  media_id: string
}

class MediaApi {
  private client: ApiClient

  constructor(client: ApiClient) {
    this.client = client
  }

  async upload(form: FormData): Promise<string> {
    const resp = await this.client.postForm<FormData, UploadResponse>("/media", form)
    return resp.media_id
  }
}

const mediaApi = new MediaApi(apiClient)
export default mediaApi
