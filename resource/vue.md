---
title: Vue
category: JavaScript libraries
---

{% raw %}

### 列表

```html
<li v-for="todo in todos">
  {{ todo.text }}
  {{ $index }}
</li>
```

### 事件

```html
<button v-on:click='submit'>Go</button>
```

### 组件

```js
new Vue({
  components: { app: App }
})
```

## API接口

```js
Vue.extend({ ... })        // creating components
Vue.nextTick(() => {...})

Vue.set(object, key, val)  // reactive
Vue.delete(object, key)

Vue.directive('my-dir', { bind, update, unbind })
// <div v-my-dir='...'></div>

Vue.elementDirective('my-dir', { bind, update, unbind })
// <my-dir>...</my-dir>

Vue.component('my-component', Vue.extend({ .. }))

Vue.partial('my-partial', '<div>hi {{msg}}</div>')
// <partial name='my-partial'></partial>
```

```js
new Vue({
  data: { ... }
  props: ['size'],
  props: { size: Number },
  computed: { fullname() { return this.name + ' ' + this.lastName } },
  methods: { go() { ... } },
  watch: { a (val, oldVal) { ... } },
  el: '#foo',
  template: '...',
  replace: true, // replace element (default true)

  // lifecycle
  created () {},
  beforeCompile () {},
  compiled () {},
  ready () {}, // $el is inserted for the first time
  attached () {},
  detached () {},
  beforeDestroy () {},
  destroyed () {},

  // options
  directives: {},
  elementDirectives: {},
  filters: {},
  components: {},
  transitions: {},
  partials: {}
})
```

## Vue模板
参考 [vueify](https://www.npmjs.com/package/vueify)

```js
// app.vue
<template>
  <h1 class="red">{{msg}}</h1>
</template>
 
<script>
  module.exports = {
    data () {
      return {
        msg: 'Hello world!'
      }
    }
  }
</script> 
```

以及

```html
<template lang='jade'>
h1(class='red') {{msg}}
</template>
```

{% endraw %}