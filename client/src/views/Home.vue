<template>
  <div class="home">

    <v-container class="my-5">

      <v-toolbar flat class="white">
        <v-toolbar-title>图书列表</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-dialog v-model="dialog" max-width="600px">
          <v-btn slot="activator" class="primary" dark>新增</v-btn>
          <v-card>
            <v-card-title>
              <span class="headline">{{ formTitle }}</span>
            </v-card-title>
            <v-card-text>
              <v-alert :value="Boolean(errMsg)" color="error" icon="warning" outline>
                {{ errMsg }}
              </v-alert>
              <v-container grid-list-md>
                <v-layout>
                  <v-flex xs12 sm12 md6>
                    <v-text-field label="书名" v-model="editedItem.name"></v-text-field>
                  </v-flex>
                  <v-flex xs12 sm12 md6>
                    <v-text-field label="分类" v-model="editedItem.category"></v-text-field>
                  </v-flex>
                </v-layout>
              </v-container>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" flat @click="close">取消</v-btn>
              <v-btn color="blue darken-1" flat @click="save">保存</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>

      <v-data-table
        :headers="headers"
        :items="books"
        hide-actions
        class="elevation-1"
      >
        <template slot="items" slot-scope="props">
          <td>{{ props.item.name }}</td>
          <td>{{ props.item.category }}</td>
          <td class="layout px-0">
            <v-icon small class="ml-4" @click="editItem(props.item)">
              edit
            </v-icon>
            <v-icon small @click="deleteItem(props.item)">
              delete
            </v-icon>
          </td>
        </template>
        <template slot="no-data">
          <v-alert :value="true" color="info" outline>
            无数据
          </v-alert>
        </template>
      </v-data-table>
    </v-container>

  </div>
</template>

<script>
  export default {
    data: () => ({
      headers: [
        { text: '书名', value: 'name', sortable: false, align: 'left'},
        { text: '分类', value: 'category', sortable: false },
        { text: '操作', value: 'name', sortable: false }
      ],
      books: [],
      dialog: false, // 是否展示对话框
      errMsg: '', // 是否有错误信息
      editedIndex: -1, // 当前编辑的图书在列表中的序号
      editedItem: { // 当前编辑的图书内容
        id: 0,
        name: '',
        category: ''
      },
      defaultItem: { // 默认的图书内容
        id: 0,
        name: '',
        category: ''
      }
    }),
    computed: {
      formTitle () {
        return this.editedIndex === -1 ? '新增' : '编辑'
      }
    },
    watch: {
      dialog (val) {
        if (!val) {
          this.close()
          this.clearErrMsg()
        }
      }
    },
    methods: {
      close () {
        this.dialog = false
        setTimeout(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        }, 300)
      },
      clearErrMsg () {
        this.errMsg = ''
      },

      save() {
        if (this.editedIndex > -1) { // 编辑
          Object.assign(this.books[this.editedIndex], this.editedItem)
        } else { // 新增
          this.books.push(this.editedItem)
        }
        this.close()
      },
      editItem (item) {
        this.editedIndex = this.books.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },
      deleteItem (item) {
        const index = this.books.indexOf(item)
        confirm('确认删除?') && this.books.splice(index, 1)
      },
    },
    created () {
      this.books = [
        { name: '生死疲劳', category: '文学' },
        { name: '国家宝藏', category: '人文社科' },
        { name: '人类简史', category: '科技' },
      ]
    },
  }
</script>
