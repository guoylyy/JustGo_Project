﻿#pragma checksum "C:\Users\Jian\Documents\GitHub\JustGo_Project\JustGo_WP\Archive\Archive\Pages\GoalDetailPage.xaml" "{406ea660-64cf-4c82-b6f0-42d48172a799}" "A33B4CF158A4BB46B8DE55A043FD524A"
//------------------------------------------------------------------------------
// <auto-generated>
//     此代码由工具生成。
//     运行时版本:4.0.30319.34014
//
//     对此文件的更改可能会导致不正确的行为，并且如果
//     重新生成代码，这些更改将会丢失。
// </auto-generated>
//------------------------------------------------------------------------------

using Microsoft.Phone.Controls;
using System;
using System.Windows;
using System.Windows.Automation;
using System.Windows.Automation.Peers;
using System.Windows.Automation.Provider;
using System.Windows.Controls;
using System.Windows.Controls.Primitives;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Ink;
using System.Windows.Input;
using System.Windows.Interop;
using System.Windows.Markup;
using System.Windows.Media;
using System.Windows.Media.Animation;
using System.Windows.Media.Imaging;
using System.Windows.Resources;
using System.Windows.Shapes;
using System.Windows.Threading;


namespace Archive.Pages {
    
    
    public partial class GoalDetailPage : Microsoft.Phone.Controls.PhoneApplicationPage {
        
        internal System.Windows.Controls.Grid LayoutRoot;
        
        internal System.Windows.Controls.Grid ContentGrid;
        
        internal System.Windows.Controls.TextBlock GoalNameBlock;
        
        internal System.Windows.Controls.Button JoinButton;
        
        internal System.Windows.Controls.TextBlock JoinedTextBlock;
        
        internal System.Windows.Controls.TextBlock DescriptionBlock;
        
        internal Microsoft.Phone.Controls.LongListSelector RecordsList;
        
        internal System.Windows.Controls.Grid ProgressGrid;
        
        private bool _contentLoaded;
        
        /// <summary>
        /// InitializeComponent
        /// </summary>
        [System.Diagnostics.DebuggerNonUserCodeAttribute()]
        public void InitializeComponent() {
            if (_contentLoaded) {
                return;
            }
            _contentLoaded = true;
            System.Windows.Application.LoadComponent(this, new System.Uri("/Archive;component/Pages/GoalDetailPage.xaml", System.UriKind.Relative));
            this.LayoutRoot = ((System.Windows.Controls.Grid)(this.FindName("LayoutRoot")));
            this.ContentGrid = ((System.Windows.Controls.Grid)(this.FindName("ContentGrid")));
            this.GoalNameBlock = ((System.Windows.Controls.TextBlock)(this.FindName("GoalNameBlock")));
            this.JoinButton = ((System.Windows.Controls.Button)(this.FindName("JoinButton")));
            this.JoinedTextBlock = ((System.Windows.Controls.TextBlock)(this.FindName("JoinedTextBlock")));
            this.DescriptionBlock = ((System.Windows.Controls.TextBlock)(this.FindName("DescriptionBlock")));
            this.RecordsList = ((Microsoft.Phone.Controls.LongListSelector)(this.FindName("RecordsList")));
            this.ProgressGrid = ((System.Windows.Controls.Grid)(this.FindName("ProgressGrid")));
        }
    }
}
