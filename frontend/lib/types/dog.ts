export type Dog = {
    id: string;
    name: string;
    birth_date: string;
    weight: number;
    color: string;
    gender: string;
    breed_code: number;
    profile_image_key: string | null;
    created_at: string;
};

export function isDogJson(data: unknown): data is Dog {
    if (!data || typeof data !== 'object') return false;

    const d = data as Record<string, unknown>;
    return (
        typeof d.id === 'string' &&
        typeof d.name === 'string' &&
        typeof d.birth_date === 'string' &&
        typeof d.weight === 'number' &&
        typeof d.color === 'string' &&
        typeof d.gender === 'string' &&
        typeof d.breed_code === 'number' &&
        (d.profile_image_key === null || typeof d.profile_image_key === 'string') &&
        typeof d.created_at === 'string'
    );
}