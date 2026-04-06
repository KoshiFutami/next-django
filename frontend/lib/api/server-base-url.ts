export function getServerApiBaseUrl(): string {
    const rawUrl = process.env.API_URL;
    if (!rawUrl) {
        throw new Error('API_URL is not set');
    }

    const url = new URL(rawUrl);
    return url.toString();
}