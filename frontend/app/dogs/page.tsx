import { fetchDogs } from "@/lib/api/dogs";
import type { Metadata } from "next";
import Link from "next/link";
import styles from "./page.module.css";

/** ビルド時に API_URL なしで静的生成されないよう、実行時フェッチにする */
export const dynamic = "force-dynamic";

export const metadata: Metadata = {
    title: "愛犬一覧 - Showcase",
    description: "登録済みの犬の一覧",
};

export default async function DogsListPage() {
    const dogs = await fetchDogs();

    return (
        <main className={styles.main}>
            <Link href="/" className={styles.back}>
                ← トップへ
            </Link>
            <h1 className={styles.heading}>愛犬一覧</h1>
            {dogs.length === 0 ? (
                <p className={styles.empty}>
                    登録されている犬はまだいません。
                </p>
            ) : (
                <ul className={styles.list}>
                    {dogs.map((dog) => (
                        <li key={dog.id}>
                            <Link
                                href={`/dogs/${dog.id}`}
                                className={styles.itemLink}
                            >
                                <p className={styles.itemTitle}>{dog.name}</p>
                                <p className={styles.itemMeta}>
                                    {dog.gender} · {dog.color} · 品種コード{" "}
                                    {dog.breed_code}
                                </p>
                            </Link>
                        </li>
                    ))}
                </ul>
            )}
        </main>
    );
}
