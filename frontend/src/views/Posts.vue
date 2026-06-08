<template>
  <el-container class="posts-container">
    <el-header>
      <div class="header-content">
        <h2>文章列表</h2>
        <div>
          <span>欢迎，{{ authStore.user?.email || '用户' }}</span>
          <el-button type="text" @click="logout">退出登录</el-button>
        </div>
      </div>
    </el-header>
    <el-main>
      <el-row>
        <el-col :span="12">
          <el-card>
            <template #header>新建文章</template>
            <el-form :model="newPost" label-width="80px">
              <el-form-item label="标题">
                <el-input v-model="newPost.title"></el-input>
              </el-form-item>
              <el-form-item label="内容">
                <el-input type="textarea" v-model="newPost.content" rows="4"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="createPost" :loading="creating">发布</el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card>
            <template #header>已有文章</template>
            <el-table :data="posts" style="width: 100%" v-loading="loading">
              <el-table-column prop="title" label="标题"></el-table-column>
              <el-table-column prop="content" label="内容" show-overflow-tooltip></el-table-column>
              <el-table-column prop="created_at" label="创建时间" width="180"></el-table-column>
            </el-table>
          </el-card>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '../stores/auth'
import { getPosts, createPost as apiCreatePost } from '../apis/post'

const router = useRouter()
const authStore = useAuthStore()
const posts = ref([])
const loading = ref(false)
const creating = ref(false)
const newPost = ref({ title: '', content: '' })

const fetchPosts = async () => {
  loading.value = true
  try {
    const res = await getPosts()
    posts.value = res.data
  } catch (err) {
    ElMessage.error('获取文章失败')
  } finally {
    loading.value = false
  }
}

const createPost = async () => {
  if (!newPost.value.title || !newPost.value.content) {
    ElMessage.warning('请填写标题和内容')
    return
  }
  creating.value = true
  try {
    await apiCreatePost(newPost.value.title, newPost.value.content)
    ElMessage.success('发布成功')
    newPost.value = { title: '', content: '' }
    await fetchPosts()
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '发布失败')
  } finally {
    creating.value = false
  }
}

const logout = () => {
  authStore.logout()
  router.push('/login')
}

onMounted(() => {
  fetchPosts()
})
</script>

<style scoped>
.posts-container {
  height: 100vh;
}
.el-header {
  background-color: #409eff;
  color: white;
  line-height: 60px;
}
.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.el-header h2 {
  margin: 0;
}
.el-main {
  background-color: #f0f2f5;
}
.el-col {
  padding: 10px;
}
</style>