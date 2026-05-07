import plotly.graph_objects as go
import plotly.express as px

def build_trend_chart(df, fund_id, index_name):
    """Build dual-axis trend chart for Fund vs Index."""
    fig = go.Figure()
    
    # Fund NAV (Primary Axis)
    fig.add_trace(go.Scatter(
        x=df['full_date'], y=df['nav_price'],
        name=f"Fund NAV ({fund_id})",
        line=dict(color='#00D4FF', width=3)
    ))
    
    # Index Price (Secondary Axis)
    fig.add_trace(go.Scatter(
        x=df['full_date'], y=df['index_price'],
        name=f"Index ({index_name})",
        line=dict(color='#808080', width=2, dash='dot'),
        yaxis='y2'
    ))
    
    fig.update_layout(
        template='plotly_dark',
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(title="Fund NAV", titlefont=dict(color="#00D4FF"), tickfont=dict(color="#00D4FF")),
        yaxis2=dict(title="Index Value", titlefont=dict(color="#808080"), tickfont=dict(color="#808080"), 
                   anchor="x", overlaying="y", side="right"),
        margin=dict(l=0, r=0, t=40, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def build_heatmap(df):
    """Build return heatmap matrix."""
    pivot_df = df.pivot(index="fund_id", columns="year_month", values="monthly_return")
    
    fig = px.imshow(
        pivot_df,
        labels=dict(x="Month", y="Fund ID", color="Return %"),
        x=pivot_df.columns,
        y=pivot_df.index,
        color_continuous_scale="RdYlGn",
        aspect="auto"
    )
    
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=40, b=0)
    )
    return fig

def build_performance_bar(df):
    """Build comparison bar chart for period performance."""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['period'], y=df['fund_return'],
        name='Fund Return',
        marker_color='#00D4FF'
    ))
    
    fig.add_trace(go.Bar(
        x=df['period'], y=df['index_return'],
        name='Index Return',
        marker_color='#808080'
    ))
    
    fig.update_layout(
        template='plotly_dark',
        barmode='group',
        margin=dict(l=0, r=0, t=40, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig
