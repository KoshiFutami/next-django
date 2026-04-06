import Link from "next/link";
import styles from "./not-found.module.css";

export default function NotFound() {
  return (
    <main className={styles.main}>
      <article className={styles.card}>
        <p className={styles.code} aria-hidden>
          404
        </p>
        <h1 className={styles.title}>ページが見つかりません</h1>
        <p className={styles.lead}>
          URL が間違っているか、ページが移動または削除された可能性があります。
        </p>
        <Link href="/" className={styles.home}>
          トップへ戻る
        </Link>
      </article>
    </main>
  );
}
