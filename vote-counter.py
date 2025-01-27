import pandas as pd

spreadsheet_key = ''  # from the Google sheets Publish URL
spreadsheet_range = ''  # e.g. B6:E15

url = 'https://docs.google.com/spreadsheets/d/e/{}/pub?gid=0&single=true&output=csv'.format(spreadsheet_key)
if spreadsheet_range:
    url += '&range=' + spreadsheet_range

# TODO read this from the doc
df = pd.read_csv(url, names=['Voter', 'Vote', 'Delegate', 'Position'], index_col=0)

dups = df.index.get_duplicates()
assert not dups, "{} voted twice".format(', '.join(dups))


def fixed_point(f, df):
    """Find the fixed point of a DataFrame function."""
    while True:
        df0, df = df, f(df)
        if df.equals(df0):
            return df


def follow_delegates(df):
    """Return a new DataFrame with empty votes updated from delegates' votes."""
    # Each voter's delegate, or themself if they didn't choose a delegate
    delegates = df['Delegate'].fillna(df.index.to_series())
    delegate_vote = delegates.apply(dict(df['Vote']).__getitem__)
    return df.assign(Vote=df['Vote'].fillna(delegate_vote))


# Fill in missing votes by delegates' votes, or delegates' delegates' votes, etc.
df = fixed_point(follow_delegates, df)

# Warn (don't error) on unresolved votes.
# FIXME "voters" who entered neither a vote nor delegate should be reported separately
nas = df['Vote'].isnull().sum()
if nas:
    print("{} delegated votes did not resolve".format(nas))

counts = df['Vote'].value_counts()
print('Totals:\n{}\n'.format(counts.to_string()))

winners = counts[counts == counts[counts.idxmax()]].index
if len(winners) > 1:
    print('Winners (tie):', ', '.join(winners.index))
else:
    print('Winner:', winners[0])
