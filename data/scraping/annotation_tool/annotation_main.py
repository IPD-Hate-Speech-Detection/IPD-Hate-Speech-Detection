import pandas as pd
import argparse
import sys

def get_annotation(text):
    """Prompt user until valid input is given"""
    while True:
        print(f"\nTEXT: {text}")
        print("Enter annotation as: <language> <hate_confidence> <is_hate>")
        print(" - language: 0=English, 1=Hinglish, 2=Hindi")
        print(" - hate_confidence: float between 0 and 1")
        print(" - is_hate: 0=Non-hate, 1=Hate")
        user_input = input("Your input: ").strip()

        parts = user_input.split()
        if len(parts) != 3:
            print("⚠️ Invalid format! Please provide exactly 3 values.")
            continue

        try:
            lang = int(parts[0])
            hate_conf = float(parts[1])
            is_hate = int(parts[2])

            if lang not in [0, 1, 2]:
                print("⚠️ Language must be 0, 1, or 2.")
                continue
            if not (0.0 <= hate_conf <= 1.0):
                print("⚠️ Hate confidence must be between 0 and 1.")
                continue
            if is_hate not in [0, 1]:
                print("⚠️ is_hate must be 0 or 1.")
                continue

            return lang, hate_conf, is_hate

        except ValueError:
            print("⚠️ Invalid input types! Expected: int float int.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Annotate hate speech dataset")
    parser.add_argument("input_files", nargs="+", help="CSV file(s) containing a 'text' column")
    parser.add_argument("-o", "--output", default="annotated_comments.csv", help="Output CSV filename")
    args = parser.parse_args()

    all_data = []

    for file in args.input_files:
        try:
            df = pd.read_csv(file)
        except Exception as e:
            print(f"❌ Error reading {file}: {e}")
            sys.exit(1)

        if "text" not in df.columns:
            print(f"❌ File {file} does not have a 'text' column.")
            sys.exit(1)

        for text in df["text"].dropna():
            lang, hate_conf, is_hate = get_annotation(text)
            all_data.append({
                "text": text,
                "language": lang,
                "hate_confidence": hate_conf,
                "is_hate": is_hate
            })

    out_df = pd.DataFrame(all_data)
    out_df.to_csv(args.output, index=False, encoding="utf-8-sig")
    print(f"\n✅ Saved {len(out_df)} annotated rows to {args.output}")
