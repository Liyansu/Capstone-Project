// Centralized error handler
export function errorHandler(err, req, res, next) {
  const status = err.status || 500;
  const message = err.message || 'Internal Server Error';
  // eslint-disable-next-line no-console
  console.error(err);
  res.status(status).json({ error: message });
}
