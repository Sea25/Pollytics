import pandas as pd
import re
from difflib import get_close_matches
from typing import Optional, Tuple, List, Dict, Any

class ElectionChatbot:
    """Intelligent chatbot for Kerala Election Analysis."""
    
    def __init__(self, df: pd.DataFrame, booth_df: pd.DataFrame = None):
        self.df = df
        self.booth_df = booth_df
        
        self.districts = list(df['district'].unique()) if 'district' in df.columns else []
        self.constituencies = list(df['constituency'].unique()) if 'constituency' in df.columns else []
        self.candidates = list(df['candidate'].unique()) if 'candidate' in df.columns else []
        self.parties = list(df['party'].unique()) if 'party' in df.columns else []
        self.years = list(df['year'].unique()) if 'year' in df.columns else []
        
        self.all_locations = self.districts + self.constituencies
    
    def fuzzy_match(self, query: str, options: List[str], cutoff: float = 0.6) -> Optional[str]:
        """Find closest match for a query string."""
        if not query or not options:
            return None
        query_lower = query.lower().strip()
        for opt in options:
            if opt.lower() == query_lower:
                return opt
        matches = get_close_matches(query_lower, [o.lower() for o in options], n=1, cutoff=cutoff)
        if matches:
            for opt in options:
                if opt.lower() == matches[0]:
                    return opt
        return None
    
    def extract_year(self, text: str) -> Optional[int]:
        """Extract year from text."""
        year_match = re.search(r'\b(2023|2024|2025)\b', text)
        if year_match:
            return int(year_match.group(1))
        return None
    
    def extract_location(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract district and/or constituency from text."""
        text_lower = text.lower()
        found_district = None
        found_constituency = None
        
        for district in self.districts:
            if district.lower() in text_lower:
                found_district = district
                break
        
        for const in self.constituencies:
            if const.lower() in text_lower:
                found_constituency = const
                break
        
        if not found_district and not found_constituency:
            words = re.findall(r'\b[a-zA-Z]{4,}\b', text)
            for word in words:
                if word.lower() not in ['what', 'which', 'where', 'when', 'winner', 'votes', 'party', 'margin', 'results', 'show', 'tell', 'about', 'many', 'district', 'constituency', 'election', 'booth', 'compare', 'between']:
                    match = self.fuzzy_match(word, self.districts)
                    if match:
                        found_district = match
                        break
                    match = self.fuzzy_match(word, self.constituencies)
                    if match:
                        found_constituency = match
                        break
        
        return found_district, found_constituency
    
    def extract_candidate(self, text: str) -> Optional[str]:
        """Extract candidate name from text."""
        text_lower = text.lower()
        for candidate in self.candidates:
            if candidate.lower() in text_lower:
                return candidate
        words = re.findall(r'\b[A-Z][a-z]+\b', text)
        for word in words:
            match = self.fuzzy_match(word, self.candidates)
            if match:
                return match
        return None
    
    def extract_party(self, text: str) -> Optional[str]:
        """Extract party name from text."""
        text_upper = text.upper()
        for party in self.parties:
            if party.upper() in text_upper:
                return party
        return None
    
    def extract_booth(self, text: str) -> Optional[int]:
        """Extract booth ID from text."""
        booth_match = re.search(r'booth\s*(?:id\s*)?(\d+)', text.lower())
        if booth_match:
            return int(booth_match.group(1))
        return None
    
    def format_number(self, num: int) -> str:
        """Format number with commas."""
        return f"{num:,}"
    
    def get_winner(self, year: int = None, district: str = None, constituency: str = None) -> str:
        """Get winner for a specific location and year."""
        filtered = self.df.copy()
        
        if year:
            filtered = filtered[filtered['year'] == year]
        if district:
            filtered = filtered[filtered['district'] == district]
        if constituency:
            filtered = filtered[filtered['constituency'] == constituency]
        
        if filtered.empty:
            return None
        
        winners = filtered[filtered['winner'] == 'Yes']
        if winners.empty:
            return None
        
        return winners
    
    def get_candidate_votes(self, candidate: str, year: int = None, constituency: str = None) -> str:
        """Get vote count for a candidate."""
        filtered = self.df[self.df['candidate'] == candidate]
        
        if year:
            filtered = filtered[filtered['year'] == year]
        if constituency:
            filtered = filtered[filtered['constituency'] == constituency]
        
        if filtered.empty:
            return None
        
        return filtered
    
    def get_party_performance(self, party: str, year: int = None) -> Dict[str, Any]:
        """Get party performance stats."""
        filtered = self.df.copy()
        if year:
            filtered = filtered[filtered['year'] == year]
        
        party_data = filtered[filtered['party'] == party]
        if party_data.empty:
            return None
        
        wins = party_data[party_data['winner'] == 'Yes']
        total_votes = party_data['votes'].sum()
        
        return {
            'seats_won': len(wins),
            'total_votes': total_votes,
            'constituencies': wins['constituency'].tolist() if not wins.empty else []
        }
    
    def get_margin(self, year: int, constituency: str) -> Dict[str, Any]:
        """Get winning margin for a constituency."""
        filtered = self.df[(self.df['year'] == year) & (self.df['constituency'] == constituency)]
        
        if filtered.empty:
            return None
        
        sorted_df = filtered.sort_values('votes', ascending=False)
        if len(sorted_df) < 2:
            return None
        
        winner = sorted_df.iloc[0]
        runner_up = sorted_df.iloc[1]
        margin = winner['votes'] - runner_up['votes']
        
        return {
            'winner': winner['candidate'],
            'winner_party': winner['party'],
            'winner_votes': winner['votes'],
            'runner_up': runner_up['candidate'],
            'runner_up_party': runner_up['party'],
            'runner_up_votes': runner_up['votes'],
            'margin': margin
        }
    
    def get_closest_contest(self, year: int = None) -> Dict[str, Any]:
        """Find the closest contest."""
        filtered = self.df.copy()
        if year:
            filtered = filtered[filtered['year'] == year]
        
        min_margin = float('inf')
        closest = None
        
        for const in filtered['constituency'].unique():
            const_data = filtered[filtered['constituency'] == const]
            sorted_df = const_data.sort_values('votes', ascending=False)
            if len(sorted_df) >= 2:
                margin = sorted_df.iloc[0]['votes'] - sorted_df.iloc[1]['votes']
                if margin < min_margin:
                    min_margin = margin
                    closest = {
                        'constituency': const,
                        'winner': sorted_df.iloc[0]['candidate'],
                        'runner_up': sorted_df.iloc[1]['candidate'],
                        'margin': margin,
                        'year': sorted_df.iloc[0]['year']
                    }
        
        return closest
    
    def compare_years(self, year1: int, year2: int, constituency: str) -> Dict[str, Any]:
        """Compare results between two years."""
        data1 = self.df[(self.df['year'] == year1) & (self.df['constituency'] == constituency)]
        data2 = self.df[(self.df['year'] == year2) & (self.df['constituency'] == constituency)]
        
        if data1.empty or data2.empty:
            return None
        
        winner1 = data1[data1['winner'] == 'Yes'].iloc[0] if not data1[data1['winner'] == 'Yes'].empty else None
        winner2 = data2[data2['winner'] == 'Yes'].iloc[0] if not data2[data2['winner'] == 'Yes'].empty else None
        
        return {
            'year1': year1,
            'year2': year2,
            'constituency': constituency,
            'winner1': winner1['candidate'] if winner1 is not None else 'N/A',
            'party1': winner1['party'] if winner1 is not None else 'N/A',
            'votes1': winner1['votes'] if winner1 is not None else 0,
            'winner2': winner2['candidate'] if winner2 is not None else 'N/A',
            'party2': winner2['party'] if winner2 is not None else 'N/A',
            'votes2': winner2['votes'] if winner2 is not None else 0
        }
    
    def get_district_summary(self, district: str, year: int = None) -> Dict[str, Any]:
        """Get summary for a district."""
        filtered = self.df[self.df['district'] == district]
        if year:
            filtered = filtered[filtered['year'] == year]
        
        if filtered.empty:
            return None
        
        winners = filtered[filtered['winner'] == 'Yes']
        party_wins = winners.groupby('party').size().to_dict()
        
        return {
            'district': district,
            'total_constituencies': len(filtered['constituency'].unique()),
            'party_wins': party_wins,
            'winners': winners[['constituency', 'candidate', 'party', 'votes']].to_dict('records')
        }
    
    def get_booth_details(self, booth_id: int) -> Dict[str, Any]:
        """Get booth details if booth data exists."""
        if self.booth_df is None or self.booth_df.empty:
            return None
        
        booth_data = self.booth_df[self.booth_df['booth_id'] == booth_id]
        if booth_data.empty:
            return None
        
        booth_info = booth_data.iloc[0]
        candidates = booth_data[['candidate', 'party', 'votes']].to_dict('records')
        
        return {
            'booth_id': booth_id,
            'booth_name': booth_info.get('booth_name', 'N/A'),
            'constituency': booth_info.get('constituency', 'N/A'),
            'district': booth_info.get('district', 'N/A'),
            'total_voters': booth_info.get('total_voters', 0),
            'votes_polled': booth_info.get('votes_polled', 0),
            'candidates': candidates
        }
    
    def process_query(self, query: str) -> str:
        """Process user query and return response."""
        query_lower = query.lower().strip()
        
        year = self.extract_year(query)
        district, constituency = self.extract_location(query)
        candidate = self.extract_candidate(query)
        party = self.extract_party(query)
        booth_id = self.extract_booth(query)
        
        if booth_id:
            details = self.get_booth_details(booth_id)
            if details:
                winner = None
                max_votes = 0
                for c in details['candidates']:
                    if c['votes'] > max_votes:
                        max_votes = c['votes']
                        winner = c
                
                response = f"🏛️ **Booth {details['booth_id']}** - {details['booth_name']}\n\n"
                response += f"📍 Location: {details['constituency']}, {details['district']}\n"
                response += f"👥 Total Voters: {self.format_number(details['total_voters'])}\n"
                response += f"🗳️ Votes Polled: {self.format_number(details['votes_polled'])}\n\n"
                if winner:
                    response += f"🏆 Winner: **{winner['candidate']}** ({winner['party']}) - {self.format_number(winner['votes'])} votes"
                return response
            else:
                return f"❌ I couldn't find booth {booth_id} in the database. Try booth IDs between 1001-1140."
        
        if any(word in query_lower for word in ['who won', 'winner', 'won in', 'victory', 'elected']):
            if not year:
                year = max(self.years) if self.years else 2024
            
            winners = self.get_winner(year, district, constituency)
            if winners is not None and not winners.empty:
                if constituency:
                    w = winners.iloc[0]
                    margin_data = self.get_margin(year, constituency)
                    margin_text = f" with a margin of {self.format_number(margin_data['margin'])} votes" if margin_data else ""
                    return f"🏆 **{w['candidate']}** ({w['party']}) won in **{constituency}** in {year}{margin_text}!\n\n🗳️ Total Votes: {self.format_number(w['votes'])}"
                elif district:
                    response = f"🏆 **Winners in {district} District ({year}):**\n\n"
                    for _, w in winners.iterrows():
                        response += f"• **{w['constituency']}**: {w['candidate']} ({w['party']}) - {self.format_number(w['votes'])} votes\n"
                    return response
                else:
                    return f"Please specify a district or constituency. For example: 'Who won in Thiruvananthapuram in {year}?'"
            else:
                location = constituency or district or "the specified location"
                return f"❌ I couldn't find winner data for {location} in {year}. Please check the location name."
        
        if any(word in query_lower for word in ['runner up', 'second place', 'came second', '2nd place', 'runner-up']):
            if not year:
                year = max(self.years) if self.years else 2024
            if constituency:
                margin_data = self.get_margin(year, constituency)
                if margin_data:
                    return f"🥈 **Runner-up in {constituency} ({year}):**\n\n**{margin_data['runner_up']}** ({margin_data['runner_up_party']})\n🗳️ Votes: {self.format_number(margin_data['runner_up_votes'])}\n\nLost to {margin_data['winner']} by {self.format_number(margin_data['margin'])} votes."
            return "Please specify a constituency. For example: 'Who was the runner up in Nemom in 2024?'"
        
        if any(word in query_lower for word in ['how many votes', 'votes did', 'vote count', 'total votes']):
            if candidate:
                votes_data = self.get_candidate_votes(candidate, year, constituency)
                if votes_data is not None and not votes_data.empty:
                    if len(votes_data) == 1:
                        row = votes_data.iloc[0]
                        return f"🗳️ **{candidate}** received **{self.format_number(row['votes'])}** votes in {row['constituency']} ({row['year']})."
                    else:
                        response = f"🗳️ **Vote counts for {candidate}:**\n\n"
                        for _, row in votes_data.iterrows():
                            status = "🏆 Won" if row['winner'] == 'Yes' else "📊"
                            response += f"• {row['year']} - {row['constituency']}: {self.format_number(row['votes'])} votes {status}\n"
                        return response
            return "Please specify a candidate name. For example: 'How many votes did Suresh get in 2024?'"
        
        if any(word in query_lower for word in ['margin', 'won by', 'victory margin', 'winning margin']):
            if not year:
                year = max(self.years) if self.years else 2024
            if constituency:
                margin_data = self.get_margin(year, constituency)
                if margin_data:
                    return f"📊 **Margin in {constituency} ({year}):**\n\n🏆 Winner: **{margin_data['winner']}** ({margin_data['winner_party']}) - {self.format_number(margin_data['winner_votes'])} votes\n🥈 Runner-up: **{margin_data['runner_up']}** ({margin_data['runner_up_party']}) - {self.format_number(margin_data['runner_up_votes'])} votes\n\n📈 **Winning Margin: {self.format_number(margin_data['margin'])} votes**"
            return "Please specify a constituency. For example: 'What was the margin in Kovalam in 2024?'"
        
        if any(word in query_lower for word in ['closest', 'narrowest', 'tightest', 'nail-biter']):
            closest = self.get_closest_contest(year)
            if closest:
                return f"🔥 **Closest Contest{f' in {year}' if year else ''}:**\n\n📍 **{closest['constituency']}** ({closest['year']})\n🏆 Winner: {closest['winner']}\n🥈 Runner-up: {closest['runner_up']}\n📊 Margin: **Only {self.format_number(closest['margin'])} votes!**"
            return "❌ Couldn't find contest data."
        
        if any(word in query_lower for word in ['compare', 'comparison', 'vs', 'versus', 'difference between']):
            years_found = re.findall(r'\b(2023|2024|2025)\b', query)
            if len(years_found) >= 2 and constituency:
                year1, year2 = int(years_found[0]), int(years_found[1])
                comparison = self.compare_years(year1, year2, constituency)
                if comparison:
                    change = "🔄 Winner changed!" if comparison['winner1'] != comparison['winner2'] else "✅ Same winner"
                    return f"📊 **Comparison: {constituency}**\n\n**{year1}:**\n🏆 {comparison['winner1']} ({comparison['party1']}) - {self.format_number(comparison['votes1'])} votes\n\n**{year2}:**\n🏆 {comparison['winner2']} ({comparison['party2']}) - {self.format_number(comparison['votes2'])} votes\n\n{change}"
            return "Please specify two years and a constituency. For example: 'Compare 2023 and 2024 in Nemom'"
        
        if any(word in query_lower for word in ['party', 'seats', 'how many seats']):
            if party:
                perf = self.get_party_performance(party, year)
                if perf:
                    year_text = f" in {year}" if year else ""
                    response = f"📊 **{party} Performance{year_text}:**\n\n🏆 Seats Won: **{perf['seats_won']}**\n🗳️ Total Votes: {self.format_number(perf['total_votes'])}"
                    if perf['constituencies'] and len(perf['constituencies']) <= 5:
                        response += f"\n\n📍 Won in: {', '.join(perf['constituencies'])}"
                    return response
            return "Please specify a party. For example: 'How many seats did CPI win in 2024?'"
        
        if any(word in query_lower for word in ['results for', 'show results', 'all results', 'district summary']):
            if district:
                summary = self.get_district_summary(district, year)
                if summary:
                    year_text = f" ({year})" if year else ""
                    response = f"📊 **{district} District{year_text}:**\n\n"
                    response += f"📍 Constituencies: {summary['total_constituencies']}\n\n"
                    response += "**Party-wise Wins:**\n"
                    for party, wins in summary['party_wins'].items():
                        response += f"• {party}: {wins} seat(s)\n"
                    return response
            return "Please specify a district. For example: 'Show results for Kollam district'"
        
        if any(word in query_lower for word in ['exit poll', 'prediction', 'forecast']):
            return "🔮 **Exit Poll Predictions:**\n\nI provide analysis based on actual election results data. For exit poll predictions, please check official news sources!\n\nI can help you with:\n• Historical results (2023-2025)\n• Winner information\n• Vote margins\n• Party performance"
        
        if any(word in query_lower for word in ['help', 'what can you', 'how to use']):
            return self.get_help_message()
        
        if constituency:
            if not year:
                year = max(self.years) if self.years else 2024
            margin_data = self.get_margin(year, constituency)
            if margin_data:
                return f"📊 **{constituency} ({year}):**\n\n🏆 Winner: **{margin_data['winner']}** ({margin_data['winner_party']})\n🗳️ Votes: {self.format_number(margin_data['winner_votes'])}\n📈 Margin: {self.format_number(margin_data['margin'])} votes"
        
        if district:
            summary = self.get_district_summary(district, year)
            if summary:
                year_text = f" ({year})" if year else ""
                response = f"📊 **{district} District{year_text}:**\n\n"
                response += f"📍 {summary['total_constituencies']} constituencies\n\n"
                for party, wins in summary['party_wins'].items():
                    response += f"• {party}: {wins} seat(s)\n"
                return response
        
        return self.get_fallback_response()
    
    def get_help_message(self) -> str:
        """Return help message."""
        return """🤖 **Kerala Election Chatbot - Help**

I can answer questions about Kerala election data! Here's what you can ask:

**🏆 Winner Queries:**
• "Who won in Thiruvananthapuram in 2024?"
• "Winner of Nemom constituency"

**🗳️ Vote Queries:**
• "How many votes did Suresh get?"
• "Vote count for BJP in 2024"

**📊 Margin & Comparison:**
• "What was the margin in Kovalam?"
• "Compare 2023 and 2024 in Nemom"

**📍 District/Party Info:**
• "Show results for Kollam district"
• "How many seats did CPI win?"

**🔍 Special Queries:**
• "Which constituency had the closest contest?"
• "Who was the runner up in Alappuzha?"
• "Tell me about booth 1001"

Just type your question naturally! 💬"""
    
    def get_fallback_response(self) -> str:
        """Return fallback response."""
        return """❌ I cannot answer that question.

I can only answer questions about Kerala election data such as:

• **Winners:** "Who won in Thiruvananthapuram in 2024?"
• **Results:** "Show results for Kollam district"
• **Votes:** "How many votes did Suresh get?"
• **Margins:** "What was the margin in Nemom?"
• **Party seats:** "How many seats did CPI win?"

Type **"help"** for more examples! 💡"""
    
    def get_example_questions(self) -> List[str]:
        """Return list of example questions."""
        return [
            "Who won in Thiruvananthapuram in 2024?",
            "Show results for Kollam district",
            "What was the margin in Nemom?",
            "How many seats did CPI win in 2024?",
            "Which constituency had the closest contest?",
            "Compare 2023 and 2024 in Vattiyoorkavu"
        ]
