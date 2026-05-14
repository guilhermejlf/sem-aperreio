import { reactive } from 'vue'
import { fetchProfile, updateProfile } from '../config/api.js'

export const profileStore = reactive({
  data: null,
  loading: false,
  error: null,

  async load() {
    this.loading = true
    this.error = null
    try {
      this.data = await fetchProfile()
    } catch (err) {
      this.error = err.message
    } finally {
      this.loading = false
    }
  },

  async update(data) {
    this.loading = true
    this.error = null
    try {
      this.data = await updateProfile(data)
      return this.data
    } catch (err) {
      this.error = err.message
      throw err
    } finally {
      this.loading = false
    }
  },

  get displayName() {
    return this.data?.first_name || this.data?.username || 'Usuário'
  },

  get avatarInitial() {
    const name = this.data?.first_name || this.data?.username || 'U'
    return name.charAt(0).toUpperCase()
  },
})
