<template>
  <el-container class="register-container">
    <el-card class="register-card">
      <template #header>
        <h2>注册</h2>
      </template>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱"></el-input>
        </el-form-item>
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input type="password" v-model="form.password" placeholder="请输入密码"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleRegister" :loading="loading">注册</el-button>
          <el-button @click="$router.push('/login')">返回登录</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </el-container>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { register } from '../apis/user'

const router = useRouter()
const form = reactive({ email: '', username: '', password: '' })
const loading = ref(false)
const formRef = ref(null)

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

const rules = {
  email: [{ validator: validateEmail, trigger: 'blur' }],
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const handleRegister = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        await register(form.email, form.username, form.password)
        ElMessage.success({ message: '注册成功，请登录', duration: 3000 })
        router.push('/login')
      } catch (err) {
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
          ElMessage.error({ message: err.response?.data?.detail || '注册失败', duration: 5000, showClose: true })
        }
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<style scoped>
.register-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f0f2f5;
}
.register-card {
  width: 400px;
}
</style>