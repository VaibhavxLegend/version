# 🔧 Quick Postman Setup Fix

## The Error You're Getting:
```json
{
    "detail": [
        {
            "type": "missing",
            "loc": ["header", "authorization"],
            "msg": "Field required",
            "input": null
        }
    ]
}
```

## ✅ **Solution: Add Authorization Header in Postman**

### Method 1: Using Headers Tab
1. In Postman, select your `POST /hackrx/run` request
2. Go to the **Headers** tab
3. Add a new header:
   - **Key**: `Authorization`
   - **Value**: `Bearer cfe5d188df2d481cbc3d03128a7a93889df967f6c24be452005b2437b7f7b26a`

### Method 2: Using Authorization Tab
1. Select your `POST /hackrx/run` request
2. Go to the **Authorization** tab
3. Select **Type**: `Bearer Token`
4. **Token**: `cfe5d188df2d481cbc3d03128a7a93889df967f6c24be452005b2437b7f7b26a`

### Method 3: Manual Header Setup
**Headers to add:**
```
Authorization: Bearer cfe5d188df2d481cbc3d03128a7a93889df967f6c24be452005b2437b7f7b26a
Content-Type: application/json
Accept: application/json
```

## 🧪 **Test Request Body:**
```json
{
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": [
        "What is the grace period for premium payment?",
        "What is the waiting period for pre-existing diseases?"
    ]
}
```

## ✅ **Expected Success Response:**
```json
{
    "answers": [
        "A grace period of thirty days is provided for premium payment after the due date to renew or continue the policy without losing continuity benefits.",
        "There is a waiting period of thirty-six (36) months of continuous coverage from the first policy inception for pre-existing diseases and their direct complications to be covered."
    ]
}
```

## 🚨 **Common Mistakes to Avoid:**
1. ❌ Missing "Bearer " prefix in token
2. ❌ Extra spaces in the token
3. ❌ Using wrong header name (should be `Authorization`)
4. ❌ Not setting Content-Type to `application/json`

## 🔍 **Quick Debug Steps:**
1. Check Headers tab shows: `Authorization: Bearer cfe5d1...`
2. Check Body tab is set to `raw` and `JSON`
3. Ensure server is running on `http://localhost:8000`

Try again with the correct Authorization header! 🚀
