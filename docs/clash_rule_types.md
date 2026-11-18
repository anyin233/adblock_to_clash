# Clash规则类型说明

Web UI现在支持三种不同的Clash规则类型输出：

## 1. DOMAIN-SUFFIX (默认推荐)

**适用场景**: 最常用的规则类型

**匹配方式**: 匹配域名及其所有子域名

**示例**:
```yaml
payload:
  - DOMAIN-SUFFIX,example.com
```

**会匹配**:
- `example.com`
- `www.example.com`
- `api.example.com`
- `mail.subdomain.example.com`

---

## 2. DOMAIN

**适用场景**: 需要精确匹配特定域名

**匹配方式**: 仅精确匹配指定的域名

**示例**:
```yaml
payload:
  - DOMAIN,example.com
```

**会匹配**:
- `example.com`

**不会匹配**:
- `www.example.com`
- `api.example.com`

---

## 3. DOMAIN-KEYWORD

**适用场景**: 需要匹配包含特定关键词的域名

**匹配方式**: 匹配包含关键词的任何域名

**示例**:
```yaml
payload:
  - DOMAIN-KEYWORD,example
```

**会匹配**:
- `example.com`
- `test-example.org`
- `myexamplesite.net`
- `example-api.com`

---

## 选择建议

- **一般广告拦截**: 使用 **DOMAIN-SUFFIX**（最常用）
- **精确控制特定域名**: 使用 **DOMAIN**
- **广泛匹配包含关键词**: 使用 **DOMAIN-KEYWORD**

## 在Web UI中使用

1. 打开 http://127.0.0.1:8080
2. 输入规则源URL
3. 输入格式选择：**Adblock**
4. 输出格式选择：
   - **Clash - DOMAIN-SUFFIX** (推荐)
   - **Clash - DOMAIN**
   - **Clash - DOMAIN-KEYWORD**
5. 点击"Convert Rules"

转换后的规则会自动使用您选择的规则类型。
