<template>
  <el-container class="login-container">
    <el-card class="login-card">
      <template #header>
        <h2>登录</h2>
      </template>
      <!-- 关键：ref="formRef" 必须绑定 -->
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input type="password" v-model="form.password" placeholder="请输入密码"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleLogin" :loading="loading">登录</el-button>
          <el-button @click="$router.push('/register')">去注册</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </el-container>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '../stores/auth'
import { login } from '../apis/user'

const router = useRouter()
const authStore = useAuthStore()
const form = reactive({ email: '', password: '' })
const loading = ref(false)
const formRef = ref(null)  // 必须定义，并与模板中的 ref 同名

// 邮箱格式验证器
const validateEmail = (rule, value, callback) => {
  const emailRegex = /^[^\s@]+@([^\s@]+\.)+[^\s@]+$/
  if (!value) {
    callback(new Error('请输入邮箱'))
  } else if (!emailRegex.test(value)) {
    callback(new Error('请输入有效的邮箱地址（例如：user@example.com）'))
  } else {
    callback()
  }
}

// 验证规则
const rules = {
  email: [{ validator: validateEmail, trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const handleLogin = async () => {
  if (!formRef.value) return
  // 这里会触发所有字段的验证，包括 validateEmail
  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const res = await login(form.email, form.password)
        authStore.setAuth(res.data.access_token, { email: form.email })
        ElMessage.success({ message: '登录成功', duration: 2000 })
        router.push('/posts')
      } catch (err) {
        // 处理后端返回的422错误（如邮箱格式不对）
        if (err.response?.status === 422 && err.response?.data?.detail) {
          const errors = err.response.data.detail
          let errorMsg = ''
          if (Array.isArray(errors)) {
            errorMsg = errors.map(e => e.msg).join('；')
          } else {
            errorMsg = errors
          }
          ElMessage.error({ message: errorMsg, duration: 5000, showClose: true })
        } else {
          ElMessage.error({ message: err.response?.data?.detail || '登录失败', duration: 5000, showClose: true })
        }
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f0f2f5;
}
.login-card {
  width: 400px;
}
</style>