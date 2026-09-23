import customtkinter as ctk
from tkinter import messagebox
import pandas as pd

from analysis.analyzer import (
    load_latest_products,
    calculate_summary,
    get_best_deals
)

from database.db import get_connection


# ============================================================
# APPLICATION SETTINGS
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AmazonAnalyzer(ctk.CTk):

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(self):

        super().__init__()

        self.title("Amazon Analyzer")

        self.geometry("1400x850")

        self.minsize(
            1100,
            700
        )

        # -----------------------------
        # Colors
        # -----------------------------

        self.bg_color = "#0B0F19"
        self.sidebar_color = "#111827"
        self.card_color = "#151C2B"
        self.card_hover = "#1B2436"

        self.text_primary = "#F8FAFC"
        self.text_secondary = "#94A3B8"

        self.accent = "#38BDF8"

        self.border = "#263244"

        self.configure(
            fg_color=self.bg_color
        )

        # -----------------------------
        # Build application
        # -----------------------------

        self.create_sidebar()
        self.create_main_area()

    # ========================================================
    # SIDEBAR
    # ========================================================

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=245,
            corner_radius=0,
            fg_color=self.sidebar_color
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(
            False
        )

        # -----------------------------
        # Logo
        # -----------------------------

        logo_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        logo_frame.pack(
            fill="x",
            padx=25,
            pady=(30, 10)
        )

        logo_icon = ctk.CTkLabel(
            logo_frame,
            text="A",
            width=42,
            height=42,
            corner_radius=12,
            fg_color=self.accent,
            text_color="#07111D",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )

        logo_icon.pack(
            side="left"
        )

        logo_text_frame = ctk.CTkFrame(
            logo_frame,
            fg_color="transparent"
        )

        logo_text_frame.pack(
            side="left",
            padx=12
        )

        ctk.CTkLabel(
            logo_text_frame,
            text="Amazon",
            text_color=self.text_primary,
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            logo_text_frame,
            text="ANALYZER",
            text_color=self.accent,
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            )
        ).pack(
            anchor="w"
        )

        # -----------------------------
        # Navigation title
        # -----------------------------

        ctk.CTkLabel(
            self.sidebar,
            text="ANALYTICS",
            text_color="#64748B",
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(35, 10)
        )

        # -----------------------------
        # Navigation
        # -----------------------------

        self.nav_buttons = {}

        self.add_nav_button(
            "◉   Dashboard",
            self.show_dashboard,
            active=True
        )

        self.add_nav_button(
            "▣   Products",
            self.show_products
        )

        self.add_nav_button(
            "↗   Price Trends",
            self.show_trends
        )

        self.add_nav_button(
            "◆   Discounts",
            self.show_discounts
        )

        self.add_nav_button(
            "★   Best Deals",
            self.show_deals
        )

        self.add_nav_button(
            "▦   Categories",
            self.show_categories
        )

        # -----------------------------
        # Bottom section
        # -----------------------------

        bottom_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        bottom_frame.pack(
            side="bottom",
            fill="x",
            padx=20,
            pady=25
        )

        local_frame = ctk.CTkFrame(
            bottom_frame,
            fg_color=self.card_color,
            corner_radius=12
        )

        local_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        ctk.CTkLabel(
            local_frame,
            text="●",
            text_color="#22C55E",
            font=ctk.CTkFont(
                size=16
            )
        ).pack(
            side="left",
            padx=(12, 5),
            pady=12
        )

        local_text = ctk.CTkFrame(
            local_frame,
            fg_color="transparent"
        )

        local_text.pack(
            side="left",
            pady=8
        )

        ctk.CTkLabel(
            local_text,
            text="LOCAL MODE",
            text_color=self.text_primary,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            local_text,
            text="No API required",
            text_color=self.text_secondary,
            font=ctk.CTkFont(
                size=9
            )
        ).pack(
            anchor="w"
        )

        ctk.CTkButton(
            bottom_frame,
            text="↑   Import Dataset",
            height=38,
            corner_radius=10,
            fg_color=self.accent,
            hover_color="#0EA5E9",
            text_color="#07111D",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            command=self.import_dataset
        ).pack(
            fill="x"
        )

    # ========================================================
    # NAVIGATION BUTTON
    # ========================================================

    def add_nav_button(
        self,
        text,
        command,
        active=False
    ):

        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            height=44,
            corner_radius=9,
            anchor="w",
            fg_color=(
                self.accent
                if active
                else "transparent"
            ),
            hover_color=self.card_hover,
            text_color=(
                "#07111D"
                if active
                else self.text_secondary
            ),
            font=ctk.CTkFont(
                size=12,
                weight=(
                    "bold"
                    if active
                    else "normal"
                )
            ),
            command=command
        )

        button.pack(
            fill="x",
            padx=15,
            pady=3
        )

        self.nav_buttons[text] = button

    # ========================================================
    # ACTIVE NAVIGATION
    # ========================================================

    def set_active_nav(
        self,
        active_name
    ):

        for name, button in self.nav_buttons.items():

            if name == active_name:

                button.configure(
                    fg_color=self.accent,
                    text_color="#07111D",
                    font=ctk.CTkFont(
                        size=12,
                        weight="bold"
                    )
                )

            else:

                button.configure(
                    fg_color="transparent",
                    text_color=self.text_secondary,
                    font=ctk.CTkFont(
                        size=12,
                        weight="normal"
                    )
                )

    # ========================================================
    # MAIN AREA
    # ========================================================

    def create_main_area(self):

        self.main = ctk.CTkFrame(
            self,
            fg_color=self.bg_color,
            corner_radius=0
        )

        self.main.pack(
            side="left",
            fill="both",
            expand=True
        )

        # -----------------------------
        # Header
        # -----------------------------

        header = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=35,
            pady=(30, 10)
        )

        title_frame = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        title_frame.pack(
            side="left"
        )

        self.page_title = ctk.CTkLabel(
            title_frame,
            text="Dashboard",
            text_color=self.text_primary,
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )

        self.page_title.pack(
            anchor="w"
        )

        self.page_subtitle = ctk.CTkLabel(
            title_frame,
            text="Amazon price intelligence at a glance",
            text_color=self.text_secondary,
            font=ctk.CTkFont(
                size=13
            )
        )

        self.page_subtitle.pack(
            anchor="w",
            pady=(3, 0)
        )

        # -----------------------------
        # Search
        # -----------------------------

        self.search_entry = ctk.CTkEntry(
            header,
            width=270,
            height=40,
            corner_radius=10,
            placeholder_text="⌕  Search products...",
            border_width=1,
            border_color=self.border,
            fg_color=self.card_color,
            text_color=self.text_primary
        )

        self.search_entry.pack(
            side="right",
            padx=(15, 0)
        )

        # -----------------------------
        # Notification
        # -----------------------------

        ctk.CTkButton(
            header,
            text="◌",
            width=40,
            height=40,
            corner_radius=10,
            fg_color=self.card_color,
            hover_color=self.card_hover,
            text_color=self.text_secondary,
            font=ctk.CTkFont(
                size=18
            )
        ).pack(
            side="right"
        )

        # -----------------------------
        # Content
        # -----------------------------

        self.content = ctk.CTkScrollableFrame(
            self.main,
            fg_color="transparent"
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(10, 25)
        )

        self.build_dashboard()

    # ========================================================
    # DASHBOARD
    # ========================================================

    def build_dashboard(self):

        dataframe = load_latest_products()

        summary = calculate_summary(
            dataframe
        )

        best_deals = get_best_deals(
            dataframe,
            limit=5
        )

        best_score = 0

        if not best_deals.empty:

            best_score = float(
                best_deals["deal_score"].max()
            )

        # -----------------------------
        # KPI cards
        # -----------------------------

        stats = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        stats.pack(
            fill="x",
            pady=(0, 20)
        )

        stats.grid_columnconfigure(
            (0, 1, 2, 3),
            weight=1
        )

        self.create_stat_card(
            stats,
            "TOTAL PRODUCTS",
            str(
                summary["total_products"]
            ),
            "Live database",
            0
        )

        self.create_stat_card(
            stats,
            "AVERAGE PRICE",
            f"₹{summary['average_price']:,.0f}",
            "Current prices",
            1
        )

        self.create_stat_card(
            stats,
            "AVG. DISCOUNT",
            f"{summary['average_discount']:.1f}%",
            "Available discounts",
            2
        )

        self.create_stat_card(
            stats,
            "BEST DEAL SCORE",
            f"{best_score:.0f}/100",
            "Calculated score",
            3
        )

        # -----------------------------
        # Middle section
        # -----------------------------

        middle = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        middle.pack(
            fill="x",
            pady=(0, 20)
        )

        middle.grid_columnconfigure(
            0,
            weight=2
        )

        middle.grid_columnconfigure(
            1,
            weight=1
        )

        self.create_price_chart(
            middle
        )

        self.create_discount_panel(
            middle
        )

        # -----------------------------
        # Best deals
        # -----------------------------

        self.create_best_deals(
            best_deals
        )

    # ========================================================
    # STAT CARD
    # ========================================================

    def create_stat_card(
        self,
        parent,
        title,
        value,
        change,
        column
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color=self.card_color,
            corner_radius=14,
            border_width=1,
            border_color=self.border
        )

        card.grid(
            row=0,
            column=column,
            padx=6,
            sticky="nsew"
        )

        ctk.CTkLabel(
            card,
            text=title,
            text_color=self.text_secondary,
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=18,
            pady=(18, 5)
        )

        ctk.CTkLabel(
            card,
            text=value,
            text_color=self.text_primary,
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=18
        )

        ctk.CTkLabel(
            card,
            text=change,
            text_color="#22C55E",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=18,
            pady=(3, 16)
        )

    # ========================================================
    # CURRENT PRICE CHART
    # ========================================================

    def create_price_chart(
        self,
        parent
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color=self.card_color,
            corner_radius=14,
            border_width=1,
            border_color=self.border
        )

        card.grid(
            row=0,
            column=0,
            padx=(0, 7),
            sticky="nsew"
        )

        title_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        title_frame.pack(
            fill="x",
            padx=20,
            pady=(18, 0)
        )

        ctk.CTkLabel(
            title_frame,
            text="Current Price Snapshot",
            text_color=self.text_primary,
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            )
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            title_frame,
            text="Latest database prices",
            text_color=self.text_secondary,
            font=ctk.CTkFont(
                size=10
            )
        ).pack(
            side="right"
        )

        chart = ctk.CTkFrame(
            card,
            height=250,
            fg_color="#101724",
            corner_radius=10
        )

        chart.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        dataframe = load_latest_products()

        dataframe = dataframe.dropna(
            subset=["price"]
        ).sort_values(
            "price",
            ascending=True
        ).head(10)

        canvas = ctk.CTkCanvas(
            chart,
            bg="#101724",
            highlightthickness=0
        )

        canvas.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        def draw_chart(event=None):

            canvas.delete("all")

            width = canvas.winfo_width()
            height = canvas.winfo_height()

            if width < 100 or height < 100:
                return

            if dataframe.empty:

                canvas.create_text(
                    width / 2,
                    height / 2,
                    text="No price data available",
                    fill=self.text_secondary,
                    font=("Arial", 12)
                )

                return

            padding_x = 35
            padding_y = 25

            usable_width = (
                width - padding_x * 2
            )

            usable_height = (
                height - padding_y * 2
            )

            prices = dataframe[
                "price"
            ].tolist()

            minimum = min(prices)
            maximum = max(prices)

            if minimum == maximum:
                minimum = 0

            for i in range(5):

                y = (
                    padding_y
                    +
                    (
                        usable_height / 4
                    )
                    * i
                )

                canvas.create_line(
                    padding_x,
                    y,
                    width - padding_x,
                    y,
                    fill="#202B3D"
                )

            points = []

            for i, price in enumerate(
                prices
            ):

                if len(prices) == 1:

                    x = (
                        padding_x
                        +
                        usable_width / 2
                    )

                else:

                    x = (
                        padding_x
                        +
                        (
                            i
                            /
                            (len(prices) - 1)
                        )
                        *
                        usable_width
                    )

                if maximum == minimum:

                    y = (
                        padding_y
                        +
                        usable_height / 2
                    )

                else:

                    y = (
                        padding_y
                        +
                        usable_height
                        -
                        (
                            (
                                price - minimum
                            )
                            /
                            (
                                maximum - minimum
                            )
                        )
                        *
                        usable_height
                    )

                points.extend(
                    [x, y]
                )

            if len(points) >= 4:

                canvas.create_line(
                    points,
                    fill=self.accent,
                    width=3,
                    smooth=True
                )

            for i in range(
                0,
                len(points),
                2
            ):

                x = points[i]
                y = points[i + 1]

                canvas.create_oval(
                    x - 4,
                    y - 4,
                    x + 4,
                    y + 4,
                    fill=self.accent,
                    outline=self.accent
                )

        canvas.bind(
            "<Configure>",
            draw_chart
        )

        self.after(
            200,
            draw_chart
        )

    # ========================================================
    # DISCOUNT PANEL
    # ========================================================

    def create_discount_panel(
        self,
        parent
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color=self.card_color,
            corner_radius=14,
            border_width=1,
            border_color=self.border
        )

        card.grid(
            row=0,
            column=1,
            padx=(7, 0),
            sticky="nsew"
        )

        ctk.CTkLabel(
            card,
            text="Discount Overview",
            text_color=self.text_primary,
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 3)
        )

        ctk.CTkLabel(
            card,
            text="Top available product discounts",
            text_color=self.text_secondary,
            font=ctk.CTkFont(
                size=10
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 18)
        )

        dataframe = load_latest_products()

        dataframe = dataframe.dropna(
            subset=["discount_percentage"]
        ).sort_values(
            "discount_percentage",
            ascending=False
        ).head(5)

        if dataframe.empty:

            ctk.CTkLabel(
                card,
                text="No discount data available",
                text_color=self.text_secondary
            ).pack(
                pady=30
            )

            return

        for _, product in dataframe.iterrows():

            row = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )

            row.pack(
                fill="x",
                padx=20,
                pady=6
            )

            name = str(
                product["name"]
            )

            short_name = (
                name[:28] + "..."
                if len(name) > 28
                else name
            )

            percentage = float(
                product["discount_percentage"]
            )

            ctk.CTkLabel(
                row,
                text=short_name,
                text_color=self.text_secondary,
                font=ctk.CTkFont(
                    size=10
                )
            ).pack(
                side="left"
            )

            ctk.CTkLabel(
                row,
                text=f"{percentage:.1f}%",
                text_color=self.text_primary,
                font=ctk.CTkFont(
                    size=11,
                    weight="bold"
                )
            ).pack(
                side="right"
            )

            progress = ctk.CTkProgressBar(
                card,
                height=6,
                corner_radius=3,
                progress_color=self.accent,
                fg_color="#253044"
            )

            progress.pack(
                fill="x",
                padx=20,
                pady=(0, 4)
            )

            progress.set(
                min(
                    percentage / 100,
                    1
                )
            )

    # ========================================================
    # BEST DEALS
    # ========================================================

    def create_best_deals(
        self,
        best_deals
    ):

        card = ctk.CTkFrame(
            self.content,
            fg_color=self.card_color,
            corner_radius=14,
            border_width=1,
            border_color=self.border
        )

        card.pack(
            fill="x"
        )

        header = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(18, 10)
        )

        ctk.CTkLabel(
            header,
            text="Best Deals",
            text_color=self.text_primary,
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            )
        ).pack(
            side="left"
        )

        ctk.CTkButton(
            header,
            text="View all →",
            width=80,
            height=28,
            corner_radius=7,
            fg_color="transparent",
            hover_color=self.card_hover,
            text_color=self.accent,
            font=ctk.CTkFont(
                size=10
            ),
            command=self.show_deals
        ).pack(
            side="right"
        )

        columns = ctk.CTkFrame(
            card,
            fg_color="#101724",
            corner_radius=8
        )

        columns.pack(
            fill="x",
            padx=15,
            pady=(0, 5)
        )

               headings = [
            ("PRODUCT", 0),
            ("CURRENT PRICE", 1),
            ("DISCOUNT", 2),
            ("DEAL SCORE", 3)
        ]

        # Configure fixed column proportions
        columns.grid_columnconfigure(0, weight=5)
        columns.grid_columnconfigure(1, weight=2)
        columns.grid_columnconfigure(2, weight=2)
        columns.grid_columnconfigure(3, weight=2)

        # Table header
        for text, column in headings:

            ctk.CTkLabel(
                columns,
                text=text,
                text_color="#64748B",
                font=ctk.CTkFont(
                    size=9,
                    weight="bold"
                )
            ).grid(
                row=0,
                column=column,
                sticky="w",
                padx=15,
                pady=10
            )

        if best_deals.empty:

            ctk.CTkLabel(
                columns,
                text="No deal data available.",
                text_color=self.text_secondary
            ).grid(
                row=1,
                column=0,
                columnspan=4,
                pady=25
            )

            return

        # Product rows
        for row_index, (_, product) in enumerate(
            best_deals.iterrows(),
            start=1
        ):

            name = str(
                product["name"]
            )

            short_name = (
                name[:42] + "..."
                if len(name) > 42
                else name
            )

            price = product["price"]

            price_text = (
                f"₹{float(price):,.0f}"
                if pd.notna(price)
                else "N/A"
            )

            discount = product[
                "discount_percentage"
            ]

            discount_text = (
                f"{float(discount):.1f}%"
                if pd.notna(discount)
                else "N/A"
            )

            score = float(
                product["deal_score"]
            )

            # Product
            ctk.CTkLabel(
                columns,
                text=short_name,
                text_color=self.text_primary,
                font=ctk.CTkFont(
                    size=10,
                    weight="bold"
                ),
                anchor="w"
            ).grid(
                row=row_index,
                column=0,
                sticky="w",
                padx=15,
                pady=12
            )

            # Current Price
            ctk.CTkLabel(
                columns,
                text=price_text,
                text_color=self.text_primary,
                font=ctk.CTkFont(
                    size=11
                ),
                anchor="w"
            ).grid(
                row=row_index,
                column=1,
                sticky="w",
                padx=15,
                pady=12
            )

            # Discount
            ctk.CTkLabel(
                columns,
                text=discount_text,
                text_color="#22C55E",
                font=ctk.CTkFont(
                    size=11,
                    weight="bold"
                ),
                anchor="w"
            ).grid(
                row=row_index,
                column=2,
                sticky="w",
                padx=15,
                pady=12
            )

            # Deal Score
            ctk.CTkLabel(
                columns,
                text=f"{score:.0f}/100",
                text_color=self.accent,
                font=ctk.CTkFont(
                    size=11,
                    weight="bold"
                ),
                anchor="w"
            ).grid(
                row=row_index,
                column=3,
                sticky="w",
                padx=15,
                pady=12
            )

    # ========================================================
    # CLEAR CONTENT
    # ========================================================

    def clear_content(self):

        for widget in self.content.winfo_children():

            widget.destroy()

    # ========================================================
    # DASHBOARD
    # ========================================================

    def show_dashboard(self):

        self.set_active_nav(
            "◉   Dashboard"
        )

        self.page_title.configure(
            text="Dashboard"
        )

        self.page_subtitle.configure(
            text="Amazon price intelligence at a glance"
        )

        self.clear_content()

        self.build_dashboard()

    # ========================================================
    # PRODUCTS
    # ========================================================

    def show_products(self):

        self.set_active_nav(
            "▣   Products"
        )

        self.page_title.configure(
            text="Products"
        )

        self.page_subtitle.configure(
            text="Explore and filter product data"
        )

        self.clear_content()

        dataframe = load_latest_products()

        card = ctk.CTkFrame(
            self.content,
            fg_color=self.card_color,
            corner_radius=14,
            border_width=1,
            border_color=self.border
        )

        card.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        ctk.CTkLabel(
            card,
            text=f"Product Explorer ({len(dataframe)} products)",
            text_color=self.text_primary,
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        ctk.CTkLabel(
            card,
            text="Live data loaded from the SQLite database.",
            text_color=self.text_secondary,
            font=ctk.CTkFont(
                size=12
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

        product_area = ctk.CTkScrollableFrame(
            card,
            fg_color="transparent"
        )

        product_area.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        if dataframe.empty:

            ctk.CTkLabel(
                product_area,
                text="No products available.",
                text_color=self.text_secondary
            ).pack(
                pady=50
            )

            return

        for _, product in dataframe.iterrows():

            row = ctk.CTkFrame(
                product_area,
                fg_color="#101724",
                corner_radius=10
            )

            row.pack(
                fill="x",
                pady=5
            )

            name = str(
                product["name"]
            )

            short_name = (
                name[:90] + "..."
                if len(name) > 90
                else name
            )

            price = product["price"]
            rating = product["rating"]
            discount = product[
                "discount_percentage"
            ]

            price_text = (
                f"₹{float(price):,.0f}"
                if pd.notna(price)
                else "N/A"
            )

            rating_text = (
                f"{float(rating):.1f}/5"
                if pd.notna(rating)
                else "N/A"
            )

            discount_text = (
                f"{float(discount):.1f}%"
                if pd.notna(discount)
                else "N/A"
            )

            ctk.CTkLabel(
                row,
                text=short_name,
                text_color=self.text_primary,
                font=ctk.CTkFont(
                    size=11,
                    weight="bold"
                ),
                anchor="w"
            ).pack(
                fill="x",
                padx=15,
                pady=(12, 5)
            )

            details = ctk.CTkFrame(
                row,
                fg_color="transparent"
            )

            details.pack(
                fill="x",
                padx=15,
                pady=(0, 12)
            )

            ctk.CTkLabel(
                details,
                text=f"Price: {price_text}",
                text_color=self.accent,
                font=ctk.CTkFont(
                    size=11,
                    weight="bold"
                )
            ).pack(
                side="left"
            )

            ctk.CTkLabel(
                details,
                text=f"Discount: {discount_text}",
                text_color="#22C55E",
                font=ctk.CTkFont(
                    size=11,
                    weight="bold"
                )
            ).pack(
                side="left",
                padx=20
            )

            ctk.CTkLabel(
                details,
                text=f"Rating: {rating_text}",
                text_color=self.text_secondary,
                font=ctk.CTkFont(
                    size=11
                )
            ).pack(
                side="left"
            )

            category = product["category"]

            category_text = (
                category
                if pd.notna(category)
                else "Uncategorized"
            )

            ctk.CTkLabel(
                details,
                text=f"Category: {category_text}",
                text_color=self.text_secondary,
                font=ctk.CTkFont(
                    size=10
                )
            ).pack(
                side="left",
                padx=20
            )

            ctk.CTkLabel(
                details,
                text=f"ASIN: {product['asin']}",
                text_color=self.text_secondary,
                font=ctk.CTkFont(
                    size=10
                )
            ).pack(
                side="right"
            )

    # ========================================================
    # PRICE TRENDS
    # ========================================================

    def show_trends(self):

        self.set_active_nav(
            "↗   Price Trends"
        )

        self.page_title.configure(
            text="Price Trends"
        )

        self.page_subtitle.configure(
            text="Analyze recorded price movement"
        )

        self.clear_content()

        dataframe = load_latest_products()

        card = ctk.CTkFrame(
            self.content,
            fg_color=self.card_color,
            corner_radius=14,
            border_width=1,
            border_color=self.border
        )

        card.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        ctk.CTkLabel(
            card,
            text="Price Trend Analyzer",
            text_color=self.text_primary,
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        ctk.CTkLabel(
            card,
            text="Select a product to view its recorded price history.",
            text_color=self.text_secondary,
            font=ctk.CTkFont(
                size=12
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 15)
        )

        product_names = dataframe[
            "name"
        ].tolist()

        if not product_names:

            ctk.CTkLabel(
                card,
                text="No products available.",
                text_color=self.text_secondary
            ).pack(
                pady=50
            )

            return

        selector = ctk.CTkComboBox(
            card,
            values=product_names,
            width=650,
            height=40
        )

        selector.pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

        chart_frame = ctk.CTkFrame(
            card,
            fg_color="#101724",
            corner_radius=10
        )

        chart_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 25)
        )

        canvas = ctk.CTkCanvas(
            chart_frame,
            bg="#101724",
            highlightthickness=0
        )

        canvas.pack(
            fill="both",
            expand=True
        )

        def draw_product_history(
            event=None
        ):

            canvas.delete(
                "all"
            )

            selected_name = selector.get()

            selected = dataframe[
                dataframe["name"]
                == selected_name
            ]

            if selected.empty:
                return

            product_id = int(
                selected.iloc[0]["id"]
            )

            connection = get_connection()

            history_query = """
                SELECT
                    price,
                    recorded_at
                FROM price_history
                WHERE product_id = ?
                ORDER BY recorded_at ASC, id ASC
            """

            history = pd.read_sql_query(
                history_query,
                connection,
                params=(product_id,)
            )

            connection.close()

            width = canvas.winfo_width()
            height = canvas.winfo_height()

            if width < 150 or height < 150:
                return

            if history.empty:

                canvas.create_text(
                    width / 2,
                    height / 2,
                    text="No price history available.",
                    fill=self.text_secondary,
                    font=("Arial", 12)
                )

                return

            prices = history[
                "price"
            ].tolist()

            minimum = min(prices)
            maximum = max(prices)

            padding_x = 60
            padding_y = 40

            usable_width = (
                width
                - padding_x * 2
            )

            usable_height = (
                height
                - padding_y * 2
            )

            points = []

            for i, price in enumerate(
                prices
            ):

                if len(prices) == 1:

                    x = width / 2

                else:

                    x = (
                        padding_x
                        +
                        (
                            i
                            /
                            (len(prices) - 1)
                        )
                        *
                        usable_width
                    )

                if maximum == minimum:

                    y = (
                        padding_y
                        +
                        usable_height / 2
                    )

                else:

                    y = (
                        padding_y
                        +
                        usable_height
                        -
                        (
                            (
                                price - minimum
                            )
                            /
                            (
                                maximum - minimum
                            )
                        )
                        *
                        usable_height
                    )

                points.extend(
                    [x, y]
                )

            # Grid

            for i in range(5):

                y = (
                    padding_y
                    +
                    (
                        usable_height / 4
                    )
                    * i
                )

                canvas.create_line(
                    padding_x,
                    y,
                    width - padding_x,
                    y,
                    fill="#202B3D"
                )

            # Trend line

            if len(points) >= 4:

                canvas.create_line(
                    points,
                    fill=self.accent,
                    width=3,
                    smooth=True
                )

            # Points

            for i in range(
                0,
                len(points),
                2
            ):

                x = points[i]
                y = points[i + 1]

                canvas.create_oval(
                    x - 5,
                    y - 5,
                    x + 5,
                    y + 5,
                    fill=self.accent,
                    outline=self.accent
                )

                canvas.create_text(
                    x,
                    y - 15,
                    text=(
                        f"₹{prices[i // 2]:,.0f}"
                    ),
                    fill=self.text_primary,
                    font=("Arial", 9)
                )

            if len(prices) == 1:

                canvas.create_text(
                    width / 2,
                    height - 15,
                    text=(
                        "Only one recorded price. "
                        "Run another scrape later "
                        "to build a real trend."
                    ),
                    fill=self.text_secondary,
                    font=("Arial", 10)
                )

            else:

                canvas.create_text(
                    width / 2,
                    height - 15,
                    text=(
                        f"{len(prices)} "
                        "recorded price observations"
                    ),
                    fill=self.text_secondary,
                    font=("Arial", 10)
                )

        selector.set(
            product_names[0]
        )

        selector.bind(
            "<<ComboboxSelected>>",
            draw_product_history
        )

        canvas.bind(
            "<Configure>",
            draw_product_history
        )

        self.after(
            200,
            draw_product_history
        )

    # ========================================================
    # DISCOUNTS
    # ========================================================

    def show_discounts(self):

        self.set_active_nav(
            "◆   Discounts"
        )

        self.page_title.configure(
            text="Discount Analysis"
        )

        self.page_subtitle.configure(
            text="Analyze discounts across products"
        )

        self.clear_content()

        dataframe = load_latest_products()

        dataframe = dataframe.dropna(
            subset=["discount_percentage"]
        ).sort_values(
            "discount_percentage",
            ascending=False
        )

        card = ctk.CTkFrame(
            self.content,
            fg_color=self.card_color,
            corner_radius=14,
            border_width=1,
            border_color=self.border
        )

        card.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        average_discount = (
            dataframe[
                "discount_percentage"
            ].mean()
            if not dataframe.empty
            else 0
        )

        ctk.CTkLabel(
            card,
            text="Discount Analysis",
            text_color=self.text_primary,
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        ctk.CTkLabel(
            card,
            text=(
                f"Average available discount: "
                f"{average_discount:.1f}%"
            ),
            text_color=self.text_secondary,
            font=ctk.CTkFont(
                size=12
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

        if dataframe.empty:

            ctk.CTkLabel(
                card,
                text="No discount data available.",
                text_color=self.text_secondary
            ).pack(
                pady=50
            )

            return

        discount_area = ctk.CTkScrollableFrame(
            card,
            fg_color="transparent"
        )

        discount_area.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        for _, product in dataframe.iterrows():

            row = ctk.CTkFrame(
                discount_area,
                fg_color="#101724",
                corner_radius=10
            )

            row.pack(
                fill="x",
                pady=5
            )

            name = str(
                product["name"]
            )

            short_name = (
                name[:75] + "..."
                if len(name) > 75
                else name
            )

            discount = float(
                product[
                    "discount_percentage"
                ]
            )

            price = product["price"]

            ctk.CTkLabel(
                row,
                text=short_name,
                text_color=self.text_primary,
                font=ctk.CTkFont(
                    size=11,
                    weight="bold"
                ),
                anchor="w"
            ).pack(
                side="left",
                fill="x",
                expand=True,
                padx=15,
                pady=15
            )

            ctk.CTkLabel(
                row,
                text=(
                    f"₹{float(price):,.0f}"
                    if pd.notna(price)
                    else "N/A"
                ),
                text_color=self.text_secondary,
                font=ctk.CTkFont(
                    size=11
                )
            ).pack(
                side="right",
                padx=15
            )

            ctk.CTkLabel(
                row,
                text=f"{discount:.1f}%",
                text_color="#22C55E",
                font=ctk.CTkFont(
                    size=12,
                    weight="bold"
                )
            ).pack(
                side="right",
                padx=15
            )

    # ========================================================
    # BEST DEALS
    # ========================================================

    def show_deals(self):

        self.set_active_nav(
            "★   Best Deals"
        )

        self.page_title.configure(
            text="Best Deals"
        )

        self.page_subtitle.configure(
            text="Discover products with the strongest deal scores"
        )

        self.clear_content()

        dataframe = load_latest_products()

        best_deals = get_best_deals(
            dataframe,
            limit=10
        )

        card = ctk.CTkFrame(
            self.content,
            fg_color=self.card_color,
            corner_radius=14,
            border_width=1,
            border_color=self.border
        )

        card.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        ctk.CTkLabel(
            card,
            text="Best Deals",
            text_color=self.text_primary,
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        ctk.CTkLabel(
            card,
            text=(
                "Products ranked using the calculated "
                "deal score."
            ),
            text_color=self.text_secondary,
            font=ctk.CTkFont(
                size=12
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

        if best_deals.empty:

            ctk.CTkLabel(
                card,
                text="No deal data available.",
                text_color=self.text_secondary
            ).pack(
                pady=50
            )

            return

        deals_area = ctk.CTkScrollableFrame(
            card,
            fg_color="transparent"
        )

        deals_area.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        for index, (_, product) in enumerate(
            best_deals.iterrows(),
            start=1
        ):

            row = ctk.CTkFrame(
                deals_area,
                fg_color="#101724",
                corner_radius=10
            )

            row.pack(
                fill="x",
                pady=5
            )

            name = str(
                product["name"]
            )

            short_name = (
                name[:75] + "..."
                if len(name) > 75
                else name
            )

            price = product["price"]

            price_text = (
                f"₹{float(price):,.0f}"
                if pd.notna(price)
                else "N/A"
            )

            discount = product[
                "discount_percentage"
            ]

            discount_text = (
                f"{float(discount):.1f}%"
                if pd.notna(discount)
                else "N/A"
            )

            score = float(
                product["deal_score"]
            )

            ctk.CTkLabel(
                row,
                text=f"#{index}",
                width=35,
                text_color=self.accent,
                font=ctk.CTkFont(
                    size=12,
                    weight="bold"
                )
            ).pack(
                side="left",
                padx=(12, 5)
            )

            ctk.CTkLabel(
                row,
                text=short_name,
                text_color=self.text_primary,
                font=ctk.CTkFont(
                    size=11,
                    weight="bold"
                ),
                anchor="w"
            ).pack(
                side="left",
                fill="x",
                expand=True,
                padx=10,
                pady=15
            )

            ctk.CTkLabel(
                row,
                text=price_text,
                text_color=self.text_primary,
                font=ctk.CTkFont(
                    size=11
                )
            ).pack(
                side="right",
                padx=10
            )

            ctk.CTkLabel(
                row,
                text=discount_text,
                text_color="#22C55E",
                font=ctk.CTkFont(
                    size=11,
                    weight="bold"
                )
            ).pack(
                side="right",
                padx=10
            )

            ctk.CTkLabel(
                row,
                text=f"{score:.0f}/100",
                text_color=self.accent,
                font=ctk.CTkFont(
                    size=11,
                    weight="bold"
                )
            ).pack(
                side="right",
                padx=10
            )

    # ========================================================
    # CATEGORIES
    # ========================================================

    def show_categories(self):

        self.set_active_nav(
            "▦   Categories"
        )

        self.page_title.configure(
            text="Categories"
        )

        self.page_subtitle.configure(
            text="Compare pricing and discounts by category"
        )

        self.clear_content()

        dataframe = load_latest_products()

        if dataframe.empty:

            self.create_placeholder(
                "Category Analytics",
                "No product data is available."
            )

            return

        # Create a display category.
        # Products without a category are shown
        # as Uncategorized.

        dataframe["display_category"] = (
            dataframe["category"]
            .fillna("Uncategorized")
        )

        category_summary = (
            dataframe
            .groupby(
                "display_category"
            )
            .agg(
                products=("id", "count"),
                average_price=(
                    "price",
                    "mean"
                ),
                average_discount=(
                    "discount_percentage",
                    "mean"
                )
            )
            .reset_index()
        )

        # -----------------------------------------
        # Main card
        # -----------------------------------------

        main_card = ctk.CTkFrame(
            self.content,
            fg_color=self.card_color,
            corner_radius=14,
            border_width=1,
            border_color=self.border
        )

        main_card.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        # -----------------------------------------
        # Title
        # -----------------------------------------

        ctk.CTkLabel(
            main_card,
            text="Category Analytics",
            text_color=self.text_primary,
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        ctk.CTkLabel(
            main_card,
            text=(
                "Compare product counts, prices and "
                "discounts across categories."
            ),
            text_color=self.text_secondary,
            font=ctk.CTkFont(
                size=12
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

        # -----------------------------------------
        # Category cards
        # -----------------------------------------

        cards_frame = ctk.CTkFrame(
            main_card,
            fg_color="transparent"
        )

        cards_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        category_count = min(
            len(category_summary),
            5
        )

        for column in range(
            category_count
        ):

            cards_frame.grid_columnconfigure(
                column,
                weight=1
            )

        for index, (_, category) in enumerate(
            category_summary.head(5).iterrows()
        ):

            category_card = ctk.CTkFrame(
                cards_frame,
                fg_color="#101724",
                corner_radius=10
            )

            category_card.grid(
                row=0,
                column=index,
                padx=5,
                sticky="nsew"
            )

            category_name = str(
                category["display_category"]
            )

            average_price = (
                category["average_price"]
            )

            average_discount = (
                category["average_discount"]
            )

            ctk.CTkLabel(
                category_card,
                text=category_name,
                text_color=self.text_primary,
                font=ctk.CTkFont(
                    size=13,
                    weight="bold"
                )
            ).pack(
                anchor="w",
                padx=15,
                pady=(15, 3)
            )

            ctk.CTkLabel(
                category_card,
                text=(
                    f"{int(category['products'])} products"
                ),
                text_color=self.text_secondary,
                font=ctk.CTkFont(
                    size=10
                )
            ).pack(
                anchor="w",
                padx=15
            )

            ctk.CTkLabel(
                category_card,
                text=(
                    f"₹{average_price:,.0f}"
                    if pd.notna(average_price)
                    else "N/A"
                ),
                text_color=self.accent,
                font=ctk.CTkFont(
                    size=18,
                    weight="bold"
                )
            ).pack(
                anchor="w",
                padx=15,
                pady=(8, 0)
            )

            ctk.CTkLabel(
                category_card,
                text="Average Price",
                text_color=self.text_secondary,
                font=ctk.CTkFont(
                    size=9
                )
            ).pack(
                anchor="w",
                padx=15
            )

            ctk.CTkLabel(
                category_card,
                text=(
                    f"{average_discount:.1f}%"
                    if pd.notna(average_discount)
                    else "N/A"
                ),
                text_color="#22C55E",
                font=ctk.CTkFont(
                    size=16,
                    weight="bold"
                )
            ).pack(
                anchor="w",
                padx=15,
                pady=(8, 0)
            )

            ctk.CTkLabel(
                category_card,
                text="Average Discount",
                text_color=self.text_secondary,
                font=ctk.CTkFont(
                    size=9
                )
            ).pack(
                anchor="w",
                padx=15,
                pady=(0, 15)
            )

        # -----------------------------------------
        # Discount comparison chart
        # -----------------------------------------

        chart_card = ctk.CTkFrame(
            main_card,
            fg_color="#101724",
            corner_radius=12
        )

        chart_card.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 25)
        )

        ctk.CTkLabel(
            chart_card,
            text="Average Discount by Category",
            text_color=self.text_primary,
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 10)
        )

        canvas = ctk.CTkCanvas(
            chart_card,
            bg="#101724",
            highlightthickness=0
        )

        canvas.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        def draw_category_chart(
            event=None
        ):

            canvas.delete(
                "all"
            )

            width = canvas.winfo_width()
            height = canvas.winfo_height()

            if width < 250 or height < 180:
                return

            chart_data = category_summary.dropna(
                subset=["average_discount"]
            )

            if chart_data.empty:

                canvas.create_text(
                    width / 2,
                    height / 2,
                    text="No discount data available.",
                    fill=self.text_secondary,
                    font=("Arial", 12)
                )

                return

            categories = chart_data[
                "display_category"
            ].tolist()

            values = chart_data[
                "average_discount"
            ].tolist()

            left = 160
            right = 70
            top = 30
            bottom = 30

            usable_width = (
                width
                - left
                - right
            )

            usable_height = (
                height
                - top
                - bottom
            )

            row_height = (
                usable_height
                /
                len(values)
            )

            maximum = max(
                max(values),
                100
            )

            for i, (
                category_name,
                value
            ) in enumerate(
                zip(
                    categories,
                    values
                )
            ):

                y_center = (
                    top
                    +
                    row_height * i
                    +
                    row_height / 2
                )

                # Category label

                canvas.create_text(
                    left - 10,
                    y_center,
                    text=str(
                        category_name
                    ),
                    fill=self.text_primary,
                    anchor="e",
                    font=("Arial", 10)
                )

                # Background bar

                canvas.create_rectangle(
                    left,
                    y_center - 10,
                    left + usable_width,
                    y_center + 10,
                    fill="#253044",
                    outline=""
                )

                # Value bar

                bar_width = (
                    usable_width
                    *
                    (
                        value
                        /
                        maximum
                    )
                )

                canvas.create_rectangle(
                    left,
                    y_center - 10,
                    left + bar_width,
                    y_center + 10,
                    fill=self.accent,
                    outline=""
                )

                # Percentage label

                canvas.create_text(
                    left + bar_width + 8,
                    y_center,
                    text=f"{value:.1f}%",
                    fill=self.text_primary,
                    anchor="w",
                    font=(
                        "Arial",
                        10,
                        "bold"
                    )
                )

        canvas.bind(
            "<Configure>",
            draw_category_chart
        )

        self.after(
            200,
            draw_category_chart
        )

    # ========================================================
    # PLACEHOLDER
    # ========================================================

    def create_placeholder(
        self,
        title,
        description
    ):

        card = ctk.CTkFrame(
            self.content,
            fg_color=self.card_color,
            corner_radius=14,
            border_width=1,
            border_color=self.border
        )

        card.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        ctk.CTkLabel(
            card,
            text=title,
            text_color=self.text_primary,
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        ).pack(
            pady=(100, 10)
        )

        ctk.CTkLabel(
            card,
            text=description,
            text_color=self.text_secondary,
            font=ctk.CTkFont(
                size=13
            )
        ).pack()

    # ========================================================
    # DATASET IMPORT
    # ========================================================

    def import_dataset(self):

        messagebox.showinfo(
            "Dataset Import",
            "Dataset import will be implemented in the next phase."
        )


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":

    app = AmazonAnalyzer()

    app.mainloop()
