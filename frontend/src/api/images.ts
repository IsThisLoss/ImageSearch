import apiClient, {ApiClient} from './api'

export interface InputImage {
  title: string
  description: string
  url: string
}

export interface Image {
  id: string
  title: string
  description: string
  url: string
}

export interface Response {
  status: string
}

export interface Images {
  images: Array<Image>
}

class ImagesApi {
  private client: ApiClient

  constructor(client: ApiClient) {
    this.client = client
  }

  async getAll(): Promise<Images> {
    return this.client.get<Images>('/image')
  }

  async create(image: InputImage): Promise<Response> {
    return this.client.post<InputImage, Response>('/image', image)
  }

  async search(text: string): Promise<Images> {
    return this.client.get<Images>(`/search/image?text=${text}`)
  }

  async delete(id: string): Promise<Response> {
    return this.client.delete<Response>(`/image/${id}`)
  }
}

const imagesApi = new ImagesApi(apiClient)
export default imagesApi
