module.exports = {
  root: true,
  env: { browser: true, es2021: true },
  parser: "@typescript-eslint/parser",
  parserOptions: { ecmaVersion: 2021, sourceType: "module", ecmaFeatures: { jsx: true } },
  settings: { react: { version: "detect" } },
  plugins: ["react", "react-hooks", "@typescript-eslint"],
  extends: ["plugin:react/recommended", "plugin:@typescript-eslint/recommended"],
  rules: {
    "react/react-in-jsx-scope": "off",
    "@typescript-eslint/no-explicit-any": "off",
    "@typescript-eslint/ban-ts-comment": "off",
    "@typescript-eslint/no-unused-vars": "off"
  }
};
