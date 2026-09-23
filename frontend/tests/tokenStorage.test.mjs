import test from "node:test";
import assert from "node:assert/strict";

// Mock localStorage for node environment
const storage = new Map();
global.window = {
  localStorage: {
    getItem(k) { return storage.get(k) || null; },
    setItem(k, v) { storage.set(k, String(v)); },
    removeItem(k) { storage.delete(k); },
    clear() { storage.clear(); },
  }
};
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import ts from "typescript";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const source = fs.readFileSync(path.resolve(__dirname, "../src/services/tokenStorage.ts"), "utf-8");
const transpiled = ts.transpileModule(source, { compilerOptions: { module: ts.ModuleKind.ESNext } }).outputText;
const dataUri = `data:text/javascript;base64,${Buffer.from(transpiled).toString("base64")}`;
const { tokenStorage, TOKEN_KEYS } = await import(dataUri);

test("tokenStorage canonical keys", () => {
  assert.equal(TOKEN_KEYS.ACCESS_TOKEN, "eduvia_access_token");
  assert.equal(TOKEN_KEYS.REFRESH_TOKEN, "eduvia_refresh_token");
});

test("tokenStorage lifecycle: set, get, check, clear", () => {
  storage.clear();
  assert.equal(tokenStorage.hasAccessToken(), false);
  assert.equal(tokenStorage.getAccessToken(), null);
  assert.equal(tokenStorage.getRefreshToken(), null);

  // Set tokens
  tokenStorage.setTokens("test_access_jwt_123", "test_refresh_jwt_456");

  assert.equal(tokenStorage.hasAccessToken(), true);
  assert.equal(tokenStorage.getAccessToken(), "test_access_jwt_123");
  assert.equal(tokenStorage.getRefreshToken(), "test_refresh_jwt_456");
  assert.equal(storage.get("eduvia_access_token"), "test_access_jwt_123");
  assert.equal(storage.get("eduvia_refresh_token"), "test_refresh_jwt_456");

  // Inconsistent keys should NOT be present
  assert.equal(storage.has("access_token"), false);
  assert.equal(storage.has("token"), false);

  // Clear tokens
  tokenStorage.clearTokens();
  assert.equal(tokenStorage.hasAccessToken(), false);
  assert.equal(tokenStorage.getAccessToken(), null);
  assert.equal(tokenStorage.getRefreshToken(), null);
});

test("tokenStorage triggers onAuthExpired listeners on clearTokens", () => {
  storage.clear();
  let expiredTriggered = 0;
  const unsubscribe = tokenStorage.onAuthExpired(() => {
    expiredTriggered += 1;
  });

  tokenStorage.setTokens("jwt1", "jwt2");
  tokenStorage.clearTokens();
  assert.equal(expiredTriggered, 1);

  tokenStorage.clearTokens();
  assert.equal(expiredTriggered, 2);

  unsubscribe();
  tokenStorage.clearTokens();
  assert.equal(expiredTriggered, 2, "Unsubscribed listener should not be called again");
});
