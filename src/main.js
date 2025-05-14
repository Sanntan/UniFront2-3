import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/tailwind.css'
import { createAuth0 } from '@auth0/auth0-vue'

const app = createApp(App)

app.use(
  createAuth0({
    domain: 'домен.auth0.com',
    clientId: 'client-id',
    authorizationParams: {
      redirect_uri: window.location.origin,
    },
  })
)


app.use(router)
app.mount('#app')