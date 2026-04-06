export const apiPaths = {
    dogs: {
        list: "/api/dogs/",
        detail: (id: string) => `/api/dogs/${encodeURIComponent(id)}/`,
    },
} as const;