export const apiPaths = {
    dogs: {
        detail: (id: string) => `/api/dogs/${encodeURIComponent(id)}/`,
    }
} as const;