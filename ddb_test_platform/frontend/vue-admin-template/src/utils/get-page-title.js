import defaultSettings from '@/settings'

const title = defaultSettings.title || '测试平台V1.0'

export default function getPageTitle(pageTitle) {
  if (pageTitle) {
    return `${pageTitle} - ${title}`
  }
  return `${title}`
}
