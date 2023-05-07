import apiClient, {ApiClient} from './api'

export interface InputImage {
  title: string
  description: string
  media_id: string
}

export interface ImagePreview {
  medium: string
}

export interface ImageLink {
  orig: string
  previews: ImagePreview
}

export interface Image {
  id: string
  title: string
  description: string
  links: ImagePreview
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

  async find(offset: number, limit: number, text?: string): Promise<Images> {
    let req = `/image?offset=${offset}&limit=${limit}`
    if (text) {
      req += `&text=${text}`
    }
    return this.client.get<Images>(req)
  }

  async create(image: InputImage): Promise<Response> {
    return this.client.post<InputImage, Response>('/image', image)
  }

  async delete(id: string): Promise<Response> {
    return this.client.delete<Response>(`/image/${id}`)
  }
}

const imagesApi = new ImagesApi(apiClient)
export default imagesApi
