## 📘 API Documentation – Modrinth Watcher

### 🔹 `POST /add`

Add a mod to the monitoring list.

#### Request Body
```json
{
  "mod_id": "betterf3",
  "minecraft_version": "1.21.7"
}
```

#### Response
```json
{
  "message": "Mod added to monitoring list"
}
```

#### Status Codes
- `201 Created`: Successfully added
- `400 Bad Request`: Invalid input
- `500 Internal Server Error`: JSON file issue

---

### 🔹 `POST /remove`

Remove a mod from the list.

#### Request Body
```json
{
  "mod_id": "betterf3",
  "minecraft_version": "1.21.7"
}
```

#### Response
```json
{
  "message": "Removed betterf3-1.21.7 from watch list."
}
```

#### Status Codes
- `200 OK`: Successfully removed
- `404 Not Found`: Entry not found
- `500 Internal Server Error`: JSON file issue

---

### 🔹 `GET /list`

Returns all tracked mods or filter by version.

#### Query Parameters
| Name              | Required | Description                        |
|-------------------|----------|------------------------------------|
| `minecraft_version` | ❌       | Filter mods by version (exact match) |

#### Example (Full list)
```bash
curl http://127.0.0.1:5000/list
```

#### Example (Filter)
```bash
curl "http://127.0.0.1:5000/list?minecraft_version=1.21.7"
```

#### Error (Invalid parameter)
```bash
curl "http://127.0.0.1:5000/list?loader=fabric"
```

**Response**
```json
{
  "error": "Only 'minecraft_version' filtering is allowed."
}
```

#### Status Codes
- `200 OK`: Success
- `403 Forbidden`: Unsupported filter
- `404 Not Found`: No mods match the filter
