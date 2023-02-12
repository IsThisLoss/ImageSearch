const key = 'token'

function putToken(token: string) {
  localStorage.setItem(key, `Bearer ${token}`)
}

function getToken() {
  const token = localStorage.getItem(key)
  return token;
}

export { putToken, getToken }
