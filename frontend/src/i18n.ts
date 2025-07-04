import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

const resources = {
  zh: {
    translation: {
      'Login': '登录',
      'Logout': '退出登录',
      'Username': '用户名',
      'Password': '密码',
      'Submit': '提交',
      'Dashboard': '仪表盘',
      'Settings': '设置',
      'User Settings': '用户设置',
      'Change Password': '修改密码',
      'Delete Account': '删除账户',
      'Items': '项目',
      'Add Item': '添加项目',
      'Edit Item': '编辑项目',
      'Delete Item': '删除项目',
      'Admin': '管理员',
      'Add User': '添加用户',
      'Edit User': '编辑用户',
      'Delete User': '删除用户',
      'Not Found': '未找到页面',
      'Home': '首页',
      // ...可继续补充
    }
  },
  en: {
    translation: {
      'Login': 'Login',
      'Logout': 'Logout',
      'Username': 'Username',
      'Password': 'Password',
      'Submit': 'Submit',
      'Dashboard': 'Dashboard',
      'Settings': 'Settings',
      'User Settings': 'User Settings',
      'Change Password': 'Change Password',
      'Delete Account': 'Delete Account',
      'Items': 'Items',
      'Add Item': 'Add Item',
      'Edit Item': 'Edit Item',
      'Delete Item': 'Delete Item',
      'Admin': 'Admin',
      'Add User': 'Add User',
      'Edit User': 'Edit User',
      'Delete User': 'Delete User',
      'Not Found': 'Not Found',
      'Home': 'Home',
      // ...可继续补充
    }
  }
};

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources,
    fallbackLng: 'zh',
    lng: 'zh', // 默认中文
    interpolation: {
      escapeValue: false
    }
  });

export default i18n; 