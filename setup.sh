#!/usr/bin/env bash
set -euo pipefail

if [ ! -f "backend/.env" ]; then
  cp backend/env.example backend/.env
fi

pushd backend >/dev/null
npm install --silent
npx knex migrate:latest | cat
popd >/dev/null

echo "Backend setup complete. Start with: cd backend && npm run dev"
